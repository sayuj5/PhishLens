"""
Unit tests for the Assessment Plugin system (Phase 4).
"""
import asyncio
import pytest
from fastapi.testclient import TestClient
from backend.assessment.plugins.base import BasePlugin, FindingData, SEVERITY_WEIGHTS
from backend.assessment.plugins.checks.open_ports import OpenPortsPlugin
from backend.assessment.plugins.checks.default_services import DefaultServicesPlugin
from backend.assessment.plugins.checks.outdated_banners import OutdatedBannersPlugin
from backend.assessment.plugins.checks.excessive_ports import ExcessivePortsPlugin


# ── Plugin Unit Tests ────────────────────────────────────────────────────────

def _asset(ports):
    return {
        "id": 1, "ip_address": "10.0.0.1", "hostname": "testhost",
        "os": "Linux", "vendor": "Generic", "ports": ports,
    }


def run_plugin(plugin_cls, asset_dict, config=None):
    return asyncio.get_event_loop().run_until_complete(
        plugin_cls().run(asset_dict, config or {})
    )


class TestOpenPortsPlugin:
    def test_no_findings_for_clean_asset(self):
        asset = _asset([{"port_number": 443, "service": {}}])
        findings = run_plugin(OpenPortsPlugin, asset)
        assert len(findings) == 0

    def test_detects_telnet_as_critical(self):
        asset = _asset([{"port_number": 23, "service": {}}])
        findings = run_plugin(OpenPortsPlugin, asset)
        assert len(findings) == 1
        assert findings[0].severity == "critical"
        assert "23" in findings[0].title

    def test_detects_multiple_risky_ports(self):
        asset = _asset([
            {"port_number": 22, "service": {}},
            {"port_number": 3389, "service": {}},
            {"port_number": 6379, "service": {}},
        ])
        findings = run_plugin(OpenPortsPlugin, asset)
        # 3389 and 6379 are risky; 22 is not in the list
        assert len(findings) == 2
        severities = {f.severity for f in findings}
        assert "critical" in severities  # Redis

    def test_finding_data_has_remediation(self):
        asset = _asset([{"port_number": 21, "service": {}}])
        findings = run_plugin(OpenPortsPlugin, asset)
        assert findings[0].remediation != ""
        assert findings[0].category == "port"


class TestDefaultServicesPlugin:
    def test_detects_http(self):
        asset = _asset([{"port_number": 80, "service": {}}])
        findings = run_plugin(DefaultServicesPlugin, asset)
        assert any("HTTP" in f.title for f in findings)

    def test_no_findings_for_https_only(self):
        asset = _asset([{"port_number": 443, "service": {}}])
        findings = run_plugin(DefaultServicesPlugin, asset)
        assert len(findings) == 0

    def test_severity_weights(self):
        assert SEVERITY_WEIGHTS["critical"] > SEVERITY_WEIGHTS["high"]
        assert SEVERITY_WEIGHTS["high"] > SEVERITY_WEIGHTS["medium"]


class TestOutdatedBannersPlugin:
    def test_detects_old_openssh(self):
        asset = _asset([{
            "port_number": 22,
            "service": {"banner": "SSH-2.0-OpenSSH_7.4", "name": "ssh"},
        }])
        findings = run_plugin(OutdatedBannersPlugin, asset)
        assert len(findings) == 1
        assert "OpenSSH" in findings[0].title

    def test_no_finding_for_current_openssh(self):
        asset = _asset([{
            "port_number": 22,
            "service": {"banner": "SSH-2.0-OpenSSH_9.3", "name": "ssh"},
        }])
        findings = run_plugin(OutdatedBannersPlugin, asset)
        assert len(findings) == 0

    def test_detects_old_apache(self):
        asset = _asset([{
            "port_number": 80,
            "service": {"banner": "Apache/2.4.29 (Ubuntu)", "name": "http"},
        }])
        findings = run_plugin(OutdatedBannersPlugin, asset)
        assert any("Apache" in f.title for f in findings)


class TestExcessivePortsPlugin:
    def test_no_finding_below_threshold(self):
        asset = _asset([{"port_number": i, "service": {}} for i in range(5)])
        findings = run_plugin(ExcessivePortsPlugin, asset)
        assert len(findings) == 0

    def test_low_finding_above_threshold(self):
        asset = _asset([{"port_number": i, "service": {}} for i in range(15)])
        findings = run_plugin(ExcessivePortsPlugin, asset)
        assert len(findings) == 1
        assert findings[0].severity == "low"

    def test_high_finding_for_many_ports(self):
        asset = _asset([{"port_number": i, "service": {}} for i in range(60)])
        findings = run_plugin(ExcessivePortsPlugin, asset)
        assert len(findings) == 1
        assert findings[0].severity == "high"

    def test_custom_thresholds(self):
        asset = _asset([{"port_number": i, "service": {}} for i in range(20)])
        # Custom config: low threshold at 5
        findings = run_plugin(ExcessivePortsPlugin, asset, {"threshold_low": 5, "threshold_medium": 15, "threshold_high": 30})
        assert len(findings) == 1
        assert findings[0].severity == "medium"


# ── API Integration Tests ────────────────────────────────────────────────────

class TestAssessmentAPI:
    def test_list_plugins_requires_auth(self, client):
        r = client.get("/api/assessment/plugins")
        assert r.status_code in (401, 403)

    def test_list_plugins_authenticated(self, client, auth_headers):
        r = client.get("/api/assessment/plugins", headers=auth_headers)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)

    def test_create_and_get_policy(self, client, auth_headers):
        payload = {
            "name": "CI Test Policy",
            "description": "Auto-generated in CI",
            "enabled_categories": '["port"]',
            "plugin_ids": '[]',
            "is_default": False,
        }
        r = client.post("/api/assessment/policies", json=payload, headers=auth_headers)
        assert r.status_code == 200
        policy_id = r.json()["id"]

        r2 = client.get(f"/api/assessment/policies/{policy_id}", headers=auth_headers)
        assert r2.status_code == 200
        assert r2.json()["name"] == "CI Test Policy"

    def test_assessment_stats_empty(self, client, auth_headers):
        r = client.get("/api/assessment/statistics", headers=auth_headers)
        assert r.status_code == 200
        data = r.json()
        assert "total_jobs" in data
        assert "total_findings" in data

    def test_risk_summary_returns_list(self, client, auth_headers):
        r = client.get("/api/assessment/risk-summary", headers=auth_headers)
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_findings_list_requires_auth(self, client):
        r = client.get("/api/assessment/findings")
        assert r.status_code in (401, 403)

    def test_findings_list_authenticated(self, client, auth_headers):
        r = client.get("/api/assessment/findings", headers=auth_headers)
        assert r.status_code == 200
        assert isinstance(r.json(), list)
