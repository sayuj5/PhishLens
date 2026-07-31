"""
scheduler.py - Advanced job scheduler using APScheduler.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from typing import Optional, Callable, Awaitable
from backend.logger import discovery_logger

class Scheduler:
    def __init__(self):
        self._scheduler = AsyncIOScheduler()
        self._submit_callback: Optional[Callable[[str, str, str, Optional[int]], Awaitable[None]]] = None

    def set_callback(self, cb: Callable[[str, str, str, Optional[int]], Awaitable[None]]):
        self._submit_callback = cb

    async def _fire(self, job_id: str, target: str, job_type: str, profile_id: Optional[int] = None):
        if self._submit_callback:
            try:
                await self._submit_callback(job_id, target, job_type, profile_id)
                discovery_logger.info(f"Fired scheduled job: {job_id} target={target}")
            except Exception as e:
                discovery_logger.error(f"Scheduler error firing '{job_id}': {e}")

    def add_cron_job(self, handle: str, target: str, job_type: str, cron_expr: str, profile_id: Optional[int] = None):
        """
        cron_expr example: '*/5 * * * *' (every 5 minutes)
        """
        from apscheduler.triggers.cron import CronTrigger
        trigger = CronTrigger.from_crontab(cron_expr)
        self._scheduler.add_job(
            self._fire,
            trigger=trigger,
            id=handle,
            args=[handle, target, job_type, profile_id],
            replace_existing=True
        )
        discovery_logger.info(f"Added cron job {handle} for {target} ({cron_expr})")

    def add_interval_job(self, handle: str, target: str, job_type: str, seconds: int, profile_id: Optional[int] = None):
        self._scheduler.add_job(
            self._fire,
            'interval',
            seconds=seconds,
            id=handle,
            args=[handle, target, job_type, profile_id],
            replace_existing=True
        )
        discovery_logger.info(f"Added interval job {handle} for {target} ({seconds}s)")

    def remove_job(self, handle: str):
        if self._scheduler.get_job(handle):
            self._scheduler.remove_job(handle)
            discovery_logger.info(f"Removed job {handle}")

    def list_jobs(self):
        return self._scheduler.get_jobs()

    async def start(self):
        self._scheduler.start()
        discovery_logger.info("APScheduler started.")

    async def stop(self):
        self._scheduler.shutdown()
        discovery_logger.info("APScheduler stopped.")

# Global singleton
scheduler = Scheduler()
