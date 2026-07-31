"""
Assessment Router – REST API endpoints for Phase 4.
"""
import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.database import get_db
from backend.routers.users import oauth2_scheme
from backend.assessment.engine import engine
from backend.assessment.plugins.registry import registry

logger = logging.getLogger("blackfalcon.assessment")

router = APIRouter(
    prefix="/api/assessment",
    tags=["assessment"],
    dependencies=[Depends(oauth2_scheme)],
)


# ── Plugins ───────────────────────────────────────────────

@router.get("/plugins", response_model=List[schemas.PluginOut])
def list_plugins(db: Session = Depends(get_db)):
    """List all registered assessment plugins."""
    return db.query(models.Plugin).all()


@router.post("/plugins/{plugin_id}/toggle", response_model=schemas.PluginOut)
def toggle_plugin(plugin_id: str, db: Session = Depends(get_db)):
    """Enable or disable a plugin by its plugin_id string."""
    plugin = db.query(models.Plugin).filter(models.Plugin.plugin_id == plugin_id).first()
    if not plugin:
        raise HTTPException(404, "Plugin not found")
    plugin.is_enabled = not plugin.is_enabled
    db.commit()
    db.refresh(plugin)
    return plugin


# ── Policies ──────────────────────────────────────────────

@router.get("/policies", response_model=List[schemas.AssessmentPolicy])
def list_policies(db: Session = Depends(get_db)):
    return db.query(models.AssessmentPolicy).all()


@router.post("/policies", response_model=schemas.AssessmentPolicy)
def create_policy(policy: schemas.AssessmentPolicyCreate, db: Session = Depends(get_db)):
    db_obj = models.AssessmentPolicy(**policy.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/policies/{policy_id}", response_model=schemas.AssessmentPolicy)
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    p = db.query(models.AssessmentPolicy).filter(models.AssessmentPolicy.id == policy_id).first()
    if not p:
        raise HTTPException(404, "Policy not found")
    return p


# ── Assessment Jobs ────────────────────────────────────────

@router.post("/jobs", response_model=schemas.AssessmentJobOut, status_code=202)
async def create_assessment_job(
    payload: schemas.AssessmentJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Start an assessment job against an asset. Runs in the background."""
    asset = db.query(models.Asset).filter(models.Asset.id == payload.asset_id).first()
    if not asset:
        raise HTTPException(404, "Asset not found")

    job = models.AssessmentJob(
        asset_id=payload.asset_id,
        policy_id=payload.policy_id,
        status="pending",
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Capture id before async hand-off
    job_id = job.id

    async def _run():
        from backend.database import SessionLocal
        run_db = SessionLocal()
        try:
            run_job = run_db.query(models.AssessmentJob).filter(models.AssessmentJob.id == job_id).first()
            if run_job:
                await engine.run_job(run_db, run_job)
        except Exception as exc:
            logger.error(f"Assessment job {job_id} failed: {exc}")
            run_job = run_db.query(models.AssessmentJob).filter(models.AssessmentJob.id == job_id).first()
            if run_job:
                run_job.status = "failed"
                run_job.end_time = datetime.now(timezone.utc)
                run_db.commit()
        finally:
            run_db.close()

    background_tasks.add_task(asyncio.ensure_future, _run())
    return job


@router.get("/jobs", response_model=List[schemas.AssessmentJobOut])
def list_jobs(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.AssessmentJob)
    if status:
        q = q.filter(models.AssessmentJob.status == status)
    return q.order_by(models.AssessmentJob.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/jobs/{job_id}", response_model=schemas.AssessmentJobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    j = db.query(models.AssessmentJob).filter(models.AssessmentJob.id == job_id).first()
    if not j:
        raise HTTPException(404, "Job not found")
    return j


# ── Findings ──────────────────────────────────────────────

@router.get("/findings", response_model=List[schemas.FindingOut])
def list_findings(
    skip: int = 0,
    limit: int = 100,
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    asset_id: Optional[int] = Query(None),
    q: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """List findings with optional filters."""
    query = db.query(models.Finding)
    if severity:
        query = query.filter(models.Finding.severity == severity)
    if status:
        query = query.filter(models.Finding.status == status)
    if category:
        query = query.filter(models.Finding.category == category)
    if asset_id:
        query = query.filter(models.Finding.asset_id == asset_id)
    if q:
        query = query.filter(models.Finding.title.ilike(f"%{q}%"))
    return query.order_by(models.Finding.first_seen.desc()).offset(skip).limit(limit).all()


@router.get("/findings/{finding_id}", response_model=schemas.FindingOut)
def get_finding(finding_id: int, db: Session = Depends(get_db)):
    f = db.query(models.Finding).filter(models.Finding.id == finding_id).first()
    if not f:
        raise HTTPException(404, "Finding not found")
    return f


@router.patch("/findings/{finding_id}", response_model=schemas.FindingOut)
def update_finding_status(
    finding_id: int,
    update: schemas.FindingStatusUpdate,
    db: Session = Depends(get_db),
):
    """Update finding status (open, acknowledged, resolved, false_positive)."""
    valid = {"open", "acknowledged", "resolved", "false_positive"}
    if update.status not in valid:
        raise HTTPException(400, f"Status must be one of {valid}")

    f = db.query(models.Finding).filter(models.Finding.id == finding_id).first()
    if not f:
        raise HTTPException(404, "Finding not found")

    history = models.FindingHistory(
        finding_id=f.id,
        previous_status=f.status,
        new_status=update.status,
        note=update.note,
    )
    db.add(history)

    f.status = update.status
    if update.status == "resolved":
        f.resolved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(f)
    return f


@router.get("/assets/{asset_id}/findings", response_model=List[schemas.FindingOut])
def findings_for_asset(asset_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Finding)
        .filter(models.Finding.asset_id == asset_id)
        .order_by(models.Finding.first_seen.desc())
        .all()
    )


# ── Statistics & Risk ─────────────────────────────────────

@router.get("/statistics", response_model=schemas.AssessmentStats)
def get_assessment_statistics(db: Session = Depends(get_db)):
    total_jobs = db.query(models.AssessmentJob).count()
    completed = db.query(models.AssessmentJob).filter(models.AssessmentJob.status == "completed").count()
    running = db.query(models.AssessmentJob).filter(models.AssessmentJob.status == "running").count()

    total_f = db.query(models.Finding).count()
    open_f = db.query(models.Finding).filter(models.Finding.status == "open").count()
    crit_f = db.query(models.Finding).filter(models.Finding.severity == "critical", models.Finding.status == "open").count()
    high_f = db.query(models.Finding).filter(models.Finding.severity == "high", models.Finding.status == "open").count()
    med_f = db.query(models.Finding).filter(models.Finding.severity == "medium", models.Finding.status == "open").count()
    low_f = db.query(models.Finding).filter(models.Finding.severity == "low", models.Finding.status == "open").count()
    info_f = db.query(models.Finding).filter(models.Finding.severity == "info", models.Finding.status == "open").count()

    return schemas.AssessmentStats(
        total_jobs=total_jobs,
        completed_jobs=completed,
        running_jobs=running,
        total_findings=total_f,
        open_findings=open_f,
        critical_findings=crit_f,
        high_findings=high_f,
        medium_findings=med_f,
        low_findings=low_f,
        info_findings=info_f,
    )


@router.get("/risk-summary", response_model=List[schemas.RiskSummary])
def risk_summary(limit: int = 20, db: Session = Depends(get_db)):
    """Top assets ranked by risk score."""
    assets = (
        db.query(models.Asset)
        .filter(models.Asset.risk_score > 0)
        .order_by(models.Asset.risk_score.desc())
        .limit(limit)
        .all()
    )
    result = []
    for a in assets:
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for f in db.query(models.Finding).filter(
            models.Finding.asset_id == a.id,
            models.Finding.status == "open",
        ).all():
            if f.severity in counts:
                counts[f.severity] += 1
        result.append(schemas.RiskSummary(
            asset_id=a.id,
            ip_address=a.ip_address,
            hostname=a.hostname,
            risk_score=a.risk_score or 0.0,
            **counts,
        ))
    return result


@router.get("/report-data")
def get_report_data(db: Session = Depends(get_db)):
    """Export-ready aggregated data for report generation."""
    stats = get_assessment_statistics(db)
    risk = risk_summary(db=db, limit=50)
    recent = list_findings(limit=50, status="open", db=db)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "statistics": stats.model_dump(),
        "top_risk_assets": [r.model_dump() for r in risk],
        "recent_findings": [
            {"id": f.id, "title": f.title, "severity": f.severity, "asset_id": f.asset_id}
            for f in recent
        ],
    }
