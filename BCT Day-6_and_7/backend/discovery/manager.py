import asyncio
import ipaddress
from typing import List, Dict

from backend.logger import discovery_logger
from backend.discovery.queue import DiscoveryTask
from backend.discovery.worker import discovery_worker
from backend.discovery.events import bus
from backend.discovery.inventory import update_or_create_asset, log_discovery_result
from backend.database import SessionLocal
from backend.models import DiscoveryJob

class DiscoveryManager:
    def __init__(self, num_workers: int = 5):
        self.num_workers = num_workers
        self.queue = asyncio.Queue()
        self.workers: List[asyncio.Task] = []
        self.cancel_event = asyncio.Event()
        self.active_jobs: Dict[int, int] = {} # job_id -> remaining_tasks
        
        # Subscribe to worker results
        bus.subscribe("discovery_result", self.on_task_result)

    async def start(self):
        self.cancel_event.clear()
        for i in range(self.num_workers):
            task = asyncio.create_task(discovery_worker(i, self.queue, self.cancel_event))
            self.workers.append(task)
        discovery_logger.info(f"DiscoveryManager started with {self.num_workers} workers.")

    async def stop(self):
        discovery_logger.info("Stopping DiscoveryManager...")
        self.cancel_event.set()
        if self.workers:
            await asyncio.gather(*self.workers, return_exceptions=True)
        self.workers.clear()
        discovery_logger.info("DiscoveryManager stopped.")

    async def submit_job(self, job_id: int, target: str, job_type: str, profile_id: int = None):
        """
        Parses the target (IP or CIDR) and queues tasks.
        """
        discovery_logger.info(f"Submitting job {job_id} for target {target}")
        
        targets = []
        try:
            # Try parsing as a network/CIDR
            network = ipaddress.ip_network(target, strict=False)
            targets = [str(ip) for ip in network.hosts()]
            # If it's a single IP /32, hosts() might be empty, so handle that
            if not targets:
                targets = [str(network.network_address)]
        except ValueError:
            # Not a CIDR/IP, assume hostname
            targets = [target]
            
        # Limit to 256 hosts for safety in this mock environment
        if len(targets) > 256:
            discovery_logger.warning(f"Target {target} contains >256 hosts. Truncating to 256.")
            targets = targets[:256]
            
        self.active_jobs[job_id] = len(targets)
        
        for t in targets:
            task = DiscoveryTask(job_id=job_id, target=t, job_type=job_type, profile_id=profile_id)
            await self.queue.put(task)
            
        discovery_logger.info(f"Queued {len(targets)} tasks for job {job_id}.")

    async def on_task_result(self, result_dict: dict):
        job_id = result_dict.get("job_id")
        status = result_dict.get("status")
        data = result_dict.get("data")
        
        if job_id in self.active_jobs:
            self.active_jobs[job_id] -= 1
            
        # Save to DB if online
        if status == "success" and data:
            db = SessionLocal()
            try:
                # Correlate and update inventory
                asset = update_or_create_asset(db, data)
                # Log raw result
                log_discovery_result(db, job_id, asset.id, data)
            except Exception as e:
                discovery_logger.error(f"Failed to save asset data: {e}")
            finally:
                db.close()
                
        # Check if job is complete
        if job_id in self.active_jobs and self.active_jobs[job_id] <= 0:
            discovery_logger.info(f"Job {job_id} completed.")
            del self.active_jobs[job_id]
            
            # Update DB Job Status
            db = SessionLocal()
            try:
                job = db.query(DiscoveryJob).filter(DiscoveryJob.id == job_id).first()
                if job:
                    job.status = "completed"
                    from datetime import datetime, timezone
                    job.end_time = datetime.now(timezone.utc)
                    db.commit()
            except Exception as e:
                discovery_logger.error(f"Failed to update job status: {e}")
            finally:
                db.close()
                
            await bus.publish("discovery_complete", {"job_id": job_id})

# Global singleton
manager = DiscoveryManager()
