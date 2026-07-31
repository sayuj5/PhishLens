from pydantic import BaseModel
from typing import Optional, List

class DiscoveryTask(BaseModel):
    job_id: int
    target: str # IP, CIDR, or hostname
    job_type: str # quick, full, network
    profile_id: Optional[int] = None
    
class TaskResult(BaseModel):
    job_id: int
    target: str
    status: str # success, failed
    data: Optional[dict] = None
    error: Optional[str] = None
