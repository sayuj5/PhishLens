from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from datetime import datetime, timezone

from backend import models, schemas
from backend.database import get_db
from backend.routers.users import oauth2_scheme
from backend.discovery.manager import manager
from backend.logger import api_logger

router = APIRouter(prefix="/api/discovery", tags=["discovery"], dependencies=[Depends(oauth2_scheme)])


# ──────────────────────────────────────────────
# Job Submission
# ──────────────────────────────────────────────

@router.post("/start", response_model=schemas.DiscoveryJob, status_code=202)
async def start_discovery_job(
    job: schemas.DiscoveryJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Submit a new discovery job. Accepted immediately; runs in the background."""
    db_job = models.DiscoveryJob(
        job_type=job.job_type,
        target=job.target,
        status="running",
        start_time=datetime.now(timezone.utc),
        profile_id=job.profile_id
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    api_logger.info(f"Discovery job {db_job.id} created for target {job.target} (Profile: {job.profile_id})")

    # Submit to the worker pool asynchronously
    background_tasks.add_task(manager.submit_job, db_job.id, job.target, job.job_type, job.profile_id)

    return db_job


# ──────────────────────────────────────────────
# Job Control
# ──────────────────────────────────────────────

@router.post("/cancel/{job_id}", response_model=schemas.DiscoveryJob)
def cancel_discovery_job(job_id: int, db: Session = Depends(get_db)):
    """Mark a running job as cancelled (graceful; workers drain current task first)."""
    job = db.query(models.DiscoveryJob).filter(models.DiscoveryJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status not in ("running", "pending"):
        raise HTTPException(status_code=400, detail=f"Cannot cancel job with status '{job.status}'")

    job.status = "cancelled"
    job.end_time = datetime.now(timezone.utc)

    # Remove from in-memory tracker so workers stop feeding results
    if job_id in manager.active_jobs:
        del manager.active_jobs[job_id]

    db.commit()
    db.refresh(job)
    api_logger.info(f"Job {job_id} cancelled.")
    return job


@router.post("/pause/{job_id}", response_model=schemas.DiscoveryJob)
def pause_discovery_job(job_id: int, db: Session = Depends(get_db)):
    """Pause a running job (sets status; workers will finish their current task)."""
    job = db.query(models.DiscoveryJob).filter(models.DiscoveryJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != "running":
        raise HTTPException(status_code=400, detail=f"Can only pause running jobs")

    job.status = "paused"
    db.commit()
    db.refresh(job)
    api_logger.info(f"Job {job_id} paused.")
    return job


@router.post("/resume/{job_id}", response_model=schemas.DiscoveryJob)
async def resume_discovery_job(
    job_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Resume a paused job by re-queuing remaining targets."""
    job = db.query(models.DiscoveryJob).filter(models.DiscoveryJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != "paused":
        raise HTTPException(status_code=400, detail="Only paused jobs can be resumed")

    job.status = "running"
    db.commit()
    db.refresh(job)

    # Re-submit to worker pool
    background_tasks.add_task(manager.submit_job, job.id, job.target, job.job_type)
    api_logger.info(f"Job {job_id} resumed.")
    return job


# ──────────────────────────────────────────────
# Job Queries
# ──────────────────────────────────────────────

@router.get("/jobs", response_model=List[schemas.DiscoveryJob])
def get_discovery_jobs(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all discovery jobs, newest first."""
    return (
        db.query(models.DiscoveryJob)
        .order_by(models.DiscoveryJob.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/jobs/{job_id}", response_model=schemas.DiscoveryJob)
def get_discovery_job(job_id: int, db: Session = Depends(get_db)):
    """Retrieve a single job by ID."""
    job = db.query(models.DiscoveryJob).filter(models.DiscoveryJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/history", response_model=List[schemas.DiscoveryJob])
def get_discovery_history(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Full discovery history (completed & cancelled jobs)."""
    return (
        db.query(models.DiscoveryJob)
        .filter(models.DiscoveryJob.status.in_(["completed", "failed", "cancelled"]))
        .order_by(models.DiscoveryJob.end_time.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


# ──────────────────────────────────────────────
# Real-time Progress & Workers
# ──────────────────────────────────────────────

@router.get("/progress", response_model=List[schemas.JobProgress])
def get_discovery_progress():
    """Return real-time progress for all in-flight jobs from the worker pool."""
    progress = []
    for job_id, remaining in manager.active_jobs.items():
        progress.append(schemas.JobProgress(
            job_id=job_id,
            target="",          # could be enriched from DB if needed
            status="running",
            tasks_remaining=remaining,
            is_active=True
        ))
    return progress


@router.get("/workers", response_model=schemas.WorkerStatus)
def get_worker_status():
    """Return the current state of the worker pool."""
    return schemas.WorkerStatus(
        num_workers=manager.num_workers,
        queue_size=manager.queue.qsize(),
        active_jobs=list(manager.active_jobs.keys())
    )


# ──────────────────────────────────────────────
# Aggregate Statistics
# ──────────────────────────────────────────────

@router.get("/statistics", response_model=schemas.DiscoveryStats)
def get_discovery_statistics(db: Session = Depends(get_db)):
    """Aggregate statistics across all discovery jobs."""
    total_jobs = db.query(models.DiscoveryJob).count()
    completed = db.query(models.DiscoveryJob).filter(models.DiscoveryJob.status == "completed").count()
    running   = db.query(models.DiscoveryJob).filter(models.DiscoveryJob.status == "running").count()
    failed    = db.query(models.DiscoveryJob).filter(models.DiscoveryJob.status == "failed").count()
    assets    = db.query(models.Asset).count()
    results   = db.query(models.DiscoveryResult).count()

    return schemas.DiscoveryStats(
        total_jobs=total_jobs,
        completed_jobs=completed,
        running_jobs=running,
        failed_jobs=failed,
        total_assets_discovered=assets,
        total_results=results
    )

# ──────────────────────────────────────────────
# Profiles and Scopes
# ──────────────────────────────────────────────

@router.get("/profiles", response_model=List[schemas.ScanProfile])
def get_profiles(db: Session = Depends(get_db)):
    return db.query(models.ScanProfile).all()

@router.post("/profiles", response_model=schemas.ScanProfile)
def create_profile(profile: schemas.ScanProfileCreate, db: Session = Depends(get_db)):
    db_profile = models.ScanProfile(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/scopes", response_model=List[schemas.ScanScope])
def get_scopes(db: Session = Depends(get_db)):
    return db.query(models.ScanScope).all()

@router.post("/scopes", response_model=schemas.ScanScope)
def create_scope(scope: schemas.ScanScopeCreate, db: Session = Depends(get_db)):
    db_scope = models.ScanScope(**scope.model_dump())
    db.add(db_scope)
    db.commit()
    db.refresh(db_scope)
    return db_scope
