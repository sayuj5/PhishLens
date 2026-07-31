"""
Tests for Phase 3B – Discovery Engine Core.
Covers: inventory correlation, cache, scheduler, discovery_job state machine,
        worker pool, and REST API endpoints.
"""
import asyncio
import pytest
from datetime import datetime, timezone
from unittest.mock import patch, AsyncMock

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.database import Base, get_db
from backend import models

# ──────────────────────────────────────────────
# Test DB Setup
# ──────────────────────────────────────────────

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_discovery.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# ──────────────────────────────────────────────
# Auth Helper
# ──────────────────────────────────────────────

def get_token() -> str:
    client.post("/users/", json={"email": "disc@test.com", "password": "pw1234", "role": "admin"})
    res = client.post("/token", data={"username": "disc@test.com", "password": "pw1234"})
    return res.json().get("access_token", "")

@pytest.fixture(scope="module")
def auth_headers():
    return {"Authorization": f"Bearer {get_token()}"}

# ──────────────────────────────────────────────
# Unit – discovery_job state machine
# ──────────────────────────────────────────────

def test_job_status_valid_transition():
    from backend.discovery.discovery_job import can_transition
    assert can_transition("pending", "running") is True
    assert can_transition("running", "paused") is True
    assert can_transition("paused", "running") is True
    assert can_transition("running", "completed") is True

def test_job_status_invalid_transition():
    from backend.discovery.discovery_job import can_transition, assert_transition
    assert can_transition("completed", "running") is False
    with pytest.raises(ValueError):
        assert_transition("completed", "running")

# ──────────────────────────────────────────────
# Unit – cache
# ──────────────────────────────────────────────

def test_cache_set_get():
    from backend.discovery import cache
    cache.clear()
    cache.set("192.168.1.1", {"os": "Linux"})
    result = cache.get("192.168.1.1")
    assert result == {"os": "Linux"}

def test_cache_miss():
    from backend.discovery import cache
    cache.clear()
    assert cache.get("10.0.0.1") is None

def test_cache_invalidate():
    from backend.discovery import cache
    cache.set("10.0.0.2", {"os": "Windows"})
    cache.invalidate("10.0.0.2")
    assert cache.get("10.0.0.2") is None

# ──────────────────────────────────────────────
# Unit – progress snapshot
# ──────────────────────────────────────────────

def test_progress_snapshot_percent():
    from backend.discovery.progress import ProgressSnapshot
    snap = ProgressSnapshot.build(
        job_id=1, status="running",
        total_targets=10, remaining=3,
        started_at=None
    )
    assert snap.completed == 7
    assert snap.percent == 70.0

def test_progress_snapshot_zero_total():
    from backend.discovery.progress import ProgressSnapshot
    snap = ProgressSnapshot.build(job_id=2, status="running", total_targets=0, remaining=0)
    assert snap.percent == 0.0

# ──────────────────────────────────────────────
# Unit – inventory correlation
# ──────────────────────────────────────────────

def test_inventory_create_new_asset():
    from backend.discovery.inventory import update_or_create_asset
    db = TestingSessionLocal()
    asset = update_or_create_asset(db, {"ip_address": "10.10.10.1", "hostname": "newhost"})
    assert asset.id is not None
    assert asset.ip_address == "10.10.10.1"
    db.close()

def test_inventory_deduplicates_by_ip():
    from backend.discovery.inventory import update_or_create_asset
    db = TestingSessionLocal()
    first  = update_or_create_asset(db, {"ip_address": "10.10.10.2"})
    second = update_or_create_asset(db, {"ip_address": "10.10.10.2", "hostname": "found-host"})
    assert first.id == second.id  # Same record updated, not duplicated
    db.close()

def test_inventory_port_created():
    from backend.discovery.inventory import update_or_create_asset
    db = TestingSessionLocal()
    asset = update_or_create_asset(db, {
        "ip_address": "10.10.10.3",
        "ports": [{"port": 22, "protocol": "tcp", "service": "ssh"}]
    })
    db.refresh(asset)
    assert len(asset.ports) == 1
    assert asset.ports[0].service.service_name == "ssh"
    db.close()

# ──────────────────────────────────────────────
# Unit – mock fingerprint scanner
# ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_mock_scan_returns_dict():
    from backend.discovery.fingerprint import mock_scan_target
    result = await mock_scan_target("192.168.0.1", "quick")
    assert "status" in result

# ──────────────────────────────────────────────
# Integration – REST API endpoints
# ──────────────────────────────────────────────

def test_api_start_discovery(auth_headers):
    res = client.post(
        "/api/discovery/start",
        json={"job_type": "quick", "target": "192.168.1.1"},
        headers=auth_headers
    )
    assert res.status_code == 202
    body = res.json()
    assert body["status"] == "running"
    assert body["target"] == "192.168.1.1"

def test_api_get_jobs(auth_headers):
    res = client.get("/api/discovery/jobs", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_api_get_workers(auth_headers):
    res = client.get("/api/discovery/workers", headers=auth_headers)
    assert res.status_code == 200
    body = res.json()
    assert "num_workers" in body
    assert "queue_size" in body

def test_api_get_statistics(auth_headers):
    res = client.get("/api/discovery/statistics", headers=auth_headers)
    assert res.status_code == 200
    body = res.json()
    assert "total_jobs" in body
    assert "total_assets_discovered" in body

def test_api_get_progress(auth_headers):
    res = client.get("/api/discovery/progress", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_api_cancel_nonexistent_job(auth_headers):
    res = client.post("/api/discovery/cancel/99999", headers=auth_headers)
    assert res.status_code == 404

def test_api_pause_nonexistent_job(auth_headers):
    res = client.post("/api/discovery/pause/99999", headers=auth_headers)
    assert res.status_code == 404

def test_api_get_discovery_history(auth_headers):
    res = client.get("/api/discovery/history", headers=auth_headers)
    assert res.status_code == 200

def test_api_cancel_completed_job_fails(auth_headers):
    """Cannot cancel a job that is already completed."""
    db = TestingSessionLocal()
    job = models.DiscoveryJob(job_type="quick", target="10.0.0.1", status="completed")
    db.add(job)
    db.commit()
    db.refresh(job)
    job_id = job.id
    db.close()

    res = client.post(f"/api/discovery/cancel/{job_id}", headers=auth_headers)
    assert res.status_code == 400
