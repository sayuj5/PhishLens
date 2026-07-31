"""
discovery_job.py – Domain model representing the full lifecycle of a discovery job
including state machine transitions, validation, and audit helpers.
"""
from enum import Enum
from datetime import datetime, timezone
from typing import Optional


class JobStatus(str, Enum):
    PENDING   = "pending"
    RUNNING   = "running"
    PAUSED    = "paused"
    COMPLETED = "completed"
    FAILED    = "failed"
    CANCELLED = "cancelled"


# Valid state transitions
ALLOWED_TRANSITIONS = {
    JobStatus.PENDING:   {JobStatus.RUNNING, JobStatus.CANCELLED},
    JobStatus.RUNNING:   {JobStatus.PAUSED, JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED},
    JobStatus.PAUSED:    {JobStatus.RUNNING, JobStatus.CANCELLED},
    JobStatus.COMPLETED: set(),  # terminal
    JobStatus.FAILED:    set(),  # terminal
    JobStatus.CANCELLED: set(),  # terminal
}


def can_transition(current: str, target: str) -> bool:
    """Return True if the transition from current → target is valid."""
    try:
        return JobStatus(target) in ALLOWED_TRANSITIONS[JobStatus(current)]
    except (KeyError, ValueError):
        return False


def assert_transition(current: str, target: str):
    """Raise ValueError if the transition is not allowed."""
    if not can_transition(current, target):
        raise ValueError(
            f"Invalid job status transition: '{current}' → '{target}'"
        )
