"""
progress.py – Computes and caches per-job progress summaries.
"""
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ProgressSnapshot(BaseModel):
    job_id: int
    status: str
    total_targets: int
    completed: int
    remaining: int
    percent: float
    started_at: Optional[datetime] = None
    elapsed_seconds: Optional[float] = None
    estimated_seconds_remaining: Optional[float] = None

    @classmethod
    def build(
        cls,
        job_id: int,
        status: str,
        total_targets: int,
        remaining: int,
        started_at: Optional[datetime] = None
    ) -> "ProgressSnapshot":
        completed = total_targets - remaining
        percent = round((completed / total_targets * 100), 2) if total_targets > 0 else 0.0
        elapsed = None
        eta = None
        if started_at:
            elapsed = (datetime.utcnow() - started_at.replace(tzinfo=None)).total_seconds()
            if completed > 0 and remaining > 0:
                rate = completed / elapsed  # targets/sec
                eta = remaining / rate if rate > 0 else None

        return cls(
            job_id=job_id,
            status=status,
            total_targets=total_targets,
            completed=completed,
            remaining=remaining,
            percent=percent,
            started_at=started_at,
            elapsed_seconds=round(elapsed, 1) if elapsed else None,
            estimated_seconds_remaining=round(eta, 1) if eta else None
        )
