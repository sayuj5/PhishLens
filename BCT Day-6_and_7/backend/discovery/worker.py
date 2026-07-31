import asyncio
from typing import Optional

from backend.logger import discovery_logger
from backend.discovery.queue import DiscoveryTask, TaskResult
from backend.discovery.providers.tcp import TCPDiscoveryProvider
from backend.discovery.pipeline import DiscoveryPipeline
from backend.discovery.events import bus
from backend.database import SessionLocal
from backend.models import ScanProfile

async def discovery_worker(worker_id: int, queue: asyncio.Queue, cancel_event: asyncio.Event):
    """
    Background worker that consumes DiscoveryTasks from the queue.
    """
    discovery_logger.info(f"Worker {worker_id} started.")
    
    # Initialize Pipeline
    provider = TCPDiscoveryProvider()
    pipeline = DiscoveryPipeline(provider)
    
    while not cancel_event.is_set():
        try:
            # Wait for a task or cancellation
            task_task = asyncio.create_task(queue.get())
            cancel_task = asyncio.create_task(cancel_event.wait())
            
            done, pending = await asyncio.wait(
                [task_task, cancel_task], 
                return_when=asyncio.FIRST_COMPLETED
            )
            
            if cancel_task in done:
                task_task.cancel()
                break
                
            task: DiscoveryTask = task_task.result()
            cancel_task.cancel()
            
            discovery_logger.debug(f"Worker {worker_id} processing job {task.job_id} target {task.target}")
            
            # Announce progress
            await bus.publish("discovery_progress", {
                "job_id": task.job_id,
                "target": task.target,
                "status": "scanning",
                "worker_id": worker_id
            })
            
            # Perform the scan using pipeline
            try:
                # Load profile if provided
                profile = None
                if task.profile_id:
                    db = SessionLocal()
                    try:
                        profile = db.query(ScanProfile).filter(ScanProfile.id == task.profile_id).first()
                    finally:
                        db.close()
                
                scan_data = await pipeline.execute(task.target, profile)
                
                status_code = "success"
                if scan_data.get("status") == "out_of_scope":
                    status_code = "out_of_scope"
                elif scan_data.get("status") == "offline":
                    status_code = "offline"

                result = TaskResult(
                    job_id=task.job_id,
                    target=task.target,
                    status=status_code,
                    data=scan_data
                )
            except Exception as e:
                discovery_logger.error(f"Scan failed for {task.target}: {e}")
                result = TaskResult(job_id=task.job_id, target=task.target, status="error", error=str(e))
                
            # Announce completion
            await bus.publish("discovery_result", result.model_dump())
            
            queue.task_done()
            
        except asyncio.CancelledError:
            break
        except Exception as e:
            discovery_logger.error(f"Worker {worker_id} encountered an error: {e}")
            
    discovery_logger.info(f"Worker {worker_id} shutting down.")
