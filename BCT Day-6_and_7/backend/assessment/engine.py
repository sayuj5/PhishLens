"""
Assessment Engine – executes plugins against an asset and persists findings.
"""
import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from backend import models
from backend.assessment.plugins.registry import registry
from backend.assessment.plugins.base import FindingData
from backend.discovery.events import bus

logger = logging.getLogger("blackfalcon.assessment")

SEVERITY_WEIGHTS = {"critical": 10.0, "high": 7.0, "medium": 4.0, "low": 2.0, "info": 0.5}


def _build_asset_dict(asset: models.Asset) -> Dict[str, Any]:
    """Serialise an ORM Asset into a plain dict for plugin consumption."""
    return {
        "id": asset.id,
        "ip_address": asset.ip_address,
        "hostname": asset.hostname,
        "os": asset.os,
        "vendor": asset.vendor,
        "ports": [
            {
                "port_number": p.port_number,
                "protocol": p.protocol,
                "state": p.state,
                "service": {
                    "name": p.service.service_name if p.service else None,
                    "banner": p.service.banner if p.service else None,
                    "version": p.service.version if p.service else None,
                } if p.service else {},
            }
            for p in asset.ports
        ],
    }


def _upsert_finding(db: Session, job_id: int, asset_id: int,
                    plugin_db: Optional[models.Plugin], data: FindingData) -> models.Finding:
    """Insert or update a finding in the database, deduplicating by title+asset."""
    existing = (
        db.query(models.Finding)
        .filter(
            models.Finding.asset_id == asset_id,
            models.Finding.plugin_ref == (plugin_db.plugin_id if plugin_db else data.category),
            models.Finding.title == data.title,
            models.Finding.status.notin_(["resolved", "false_positive"]),
        )
        .first()
    )
    if existing:
        existing.last_seen = datetime.now(timezone.utc)
        db.commit()
        return existing

    finding = models.Finding(
        job_id=job_id,
        asset_id=asset_id,
        plugin_id=plugin_db.id if plugin_db else None,
        plugin_ref=plugin_db.plugin_id if plugin_db else data.category,
        title=data.title,
        description=data.description,
        severity=data.severity,
        category=data.category,
        evidence=data.evidence,
        remediation=data.remediation,
        references=json.dumps(data.references),
        risk_score=data.risk_score,
    )
    db.add(finding)
    db.commit()
    db.refresh(finding)
    return finding


def _record_risk_snapshot(db: Session, asset_id: int, findings: List[models.Finding]):
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        if f.severity in counts:
            counts[f.severity] += 1
    score = sum(SEVERITY_WEIGHTS.get(k, 0) * v for k, v in counts.items())
    snapshot = models.RiskScore(asset_id=asset_id, score=round(score, 2), **counts)
    db.add(snapshot)
    # Update the live risk_score on the asset too
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if asset:
        asset.risk_score = round(score, 2)
    db.commit()


class AssessmentEngine:
    """Runs enabled plugins against a single asset and stores results."""

    def __init__(self, concurrency: int = 8):
        self._sem = asyncio.Semaphore(concurrency)

    async def run_job(self, db: Session, job: models.AssessmentJob) -> None:
        asset = db.query(models.Asset).filter(models.Asset.id == job.asset_id).first()
        if not asset:
            job.status = "failed"
            db.commit()
            return

        job.status = "running"
        job.start_time = datetime.now(timezone.utc)
        db.commit()

        await bus.publish("assessment_started", {"job_id": job.id, "asset_id": job.asset_id})
        logger.info(f"Assessment job {job.id} started for asset {asset.ip_address or asset.hostname}")

        # Determine plugins to run
        policy: Optional[models.AssessmentPolicy] = job.policy
        enabled_ids: Optional[List[str]] = None
        if policy and policy.plugin_ids:
            enabled_ids = json.loads(policy.plugin_ids)

        # Ensure plugins are discovered
        if not registry._plugins:
            registry.discover()

        plugin_classes = registry.get_enabled_plugins(enabled_ids)

        asset_dict = _build_asset_dict(asset)
        all_findings: List[models.Finding] = []

        async def _run_one(plugin_cls):
            async with self._sem:
                plugin_db = (
                    db.query(models.Plugin)
                    .filter(models.Plugin.plugin_id == plugin_cls.PLUGIN_ID)
                    .first()
                )
                if plugin_db and not plugin_db.is_enabled:
                    return
                config = json.loads(plugin_db.config) if plugin_db and plugin_db.config else {}
                try:
                    instance = plugin_cls()
                    results: List[FindingData] = await instance.run(asset_dict, config)
                    for r in results:
                        f = _upsert_finding(db, job.id, asset.id, plugin_db, r)
                        all_findings.append(f)
                        await bus.publish("new_finding", {
                            "job_id": job.id,
                            "asset_id": asset.id,
                            "finding_id": f.id,
                            "severity": r.severity,
                            "title": r.title,
                        })
                except Exception as e:
                    logger.error(f"Plugin {plugin_cls.PLUGIN_ID} failed: {e}")

        tasks = [_run_one(pc) for pc in plugin_classes]
        await asyncio.gather(*tasks)

        # Severity roll-up
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for f in all_findings:
            if f.severity in counts:
                counts[f.severity] += 1

        job.findings_count = len(all_findings)
        job.critical_count = counts["critical"]
        job.high_count = counts["high"]
        job.medium_count = counts["medium"]
        job.low_count = counts["low"]
        job.info_count = counts["info"]
        job.status = "completed"
        job.end_time = datetime.now(timezone.utc)
        db.commit()

        _record_risk_snapshot(db, asset.id, all_findings)

        await bus.publish("assessment_completed", {
            "job_id": job.id,
            "asset_id": asset.id,
            "findings": len(all_findings),
            "critical": counts["critical"],
            "high": counts["high"],
        })
        logger.info(f"Assessment job {job.id} completed: {len(all_findings)} findings.")


# Global singleton
engine = AssessmentEngine()
