from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime

# --- Users ---
class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Tags ---
class TagBase(BaseModel):
    name: str
    color: Optional[str] = "#3b82f6"

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True

# --- Services & Ports ---
class ServiceBase(BaseModel):
    service_name: str
    banner: Optional[str] = None
    version: Optional[str] = None

class Service(ServiceBase):
    id: int
    port_id: int

    class Config:
        from_attributes = True

class PortBase(BaseModel):
    port_number: int
    protocol: Optional[str] = "tcp"
    state: Optional[str] = "open"

class Port(PortBase):
    id: int
    asset_id: int
    last_seen: datetime
    service: Optional[Service] = None

    class Config:
        from_attributes = True

# --- Assets ---
class AssetBase(BaseModel):
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    hostname: Optional[str] = None
    vendor: Optional[str] = None
    os: Optional[str] = None
    risk_score: Optional[float] = 0.0
    is_active: Optional[bool] = True

class AssetCreate(AssetBase):
    network_id: Optional[int] = None

class Asset(AssetBase):
    id: int
    network_id: Optional[int]
    first_seen: datetime
    last_seen: datetime
    tags: List[Tag] = []
    ports: List[Port] = []

    class Config:
        from_attributes = True

# --- Networks ---
class NetworkBase(BaseModel):
    cidr: str
    name: str
    description: Optional[str] = None

class NetworkCreate(NetworkBase):
    pass

class Network(NetworkBase):
    id: int
    created_at: datetime
    # We might not want to dump all assets in a network by default
    # assets: List[Asset] = []

    class Config:
        from_attributes = True

# --- Discovery Jobs ---
class DiscoveryJobBase(BaseModel):
    job_type: str
    target: str
    profile_id: Optional[int] = None

class DiscoveryJobCreate(DiscoveryJobBase):
    pass

class DiscoveryJob(DiscoveryJobBase):
    id: int
    status: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    created_at: datetime
    created_by: Optional[int]

    class Config:
        from_attributes = True

# --- Dashboard & Search ---
class DashboardStats(BaseModel):
    total_assets: int
    total_networks: int
    online_hosts: int
    offline_hosts: int
    active_scan_jobs: int
    completed_scans: int
    average_risk_score: float

class SearchResult(BaseModel):
    assets: List[Asset]
    networks: List[Network]

# --- Phase 3B: Discovery Progress & Workers ---
class JobProgress(BaseModel):
    job_id: int
    target: str
    status: str
    tasks_remaining: int
    is_active: bool

class WorkerStatus(BaseModel):
    num_workers: int
    queue_size: int
    active_jobs: List[int]

class DiscoveryStats(BaseModel):
    total_jobs: int
    completed_jobs: int
    running_jobs: int
    failed_jobs: int
    total_assets_discovered: int
    total_results: int

# --- Scopes & Profiles ---
class ScanScopeBase(BaseModel):
    target: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

class ScanScopeCreate(ScanScopeBase):
    pass

class ScanScope(ScanScopeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ScanProfileBase(BaseModel):
    name: str
    description: Optional[str] = None
    concurrency: Optional[int] = 100
    timeout_ms: Optional[int] = 2000
    ports: Optional[str] = "top_100"
    retry_count: Optional[int] = 1

class ScanProfileCreate(ScanProfileBase):
    pass

class ScanProfile(ScanProfileBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Phase 4: Assessment Schemas ---

class PluginOut(BaseModel):
    id: int
    plugin_id: str
    name: str
    version: str
    author: str
    category: str
    description: Optional[str] = None
    is_enabled: bool
    created_at: datetime
    class Config:
        from_attributes = True

class AssessmentPolicyBase(BaseModel):
    name: str
    description: Optional[str] = None
    enabled_categories: Optional[str] = "[]"
    plugin_ids: Optional[str] = "[]"
    is_default: Optional[bool] = False

class AssessmentPolicyCreate(AssessmentPolicyBase):
    pass

class AssessmentPolicy(AssessmentPolicyBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class AssessmentJobCreate(BaseModel):
    asset_id: int
    policy_id: Optional[int] = None

class AssessmentJobOut(BaseModel):
    id: int
    status: str
    asset_id: Optional[int]
    policy_id: Optional[int]
    findings_count: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    created_at: datetime
    class Config:
        from_attributes = True

class FindingOut(BaseModel):
    id: int
    job_id: Optional[int]
    asset_id: int
    plugin_ref: Optional[str]
    title: str
    description: Optional[str]
    severity: str
    category: str
    evidence: Optional[str]
    remediation: Optional[str]
    references: Optional[str]
    status: str
    risk_score: float
    first_seen: datetime
    last_seen: datetime
    resolved_at: Optional[datetime]
    class Config:
        from_attributes = True

class FindingStatusUpdate(BaseModel):
    status: str
    note: Optional[str] = None

class RiskSummary(BaseModel):
    asset_id: int
    ip_address: Optional[str]
    hostname: Optional[str]
    risk_score: float
    critical: int
    high: int
    medium: int
    low: int
    info: int

class AssessmentStats(BaseModel):
    total_jobs: int
    completed_jobs: int
    running_jobs: int
    total_findings: int
    open_findings: int
    critical_findings: int
    high_findings: int
    medium_findings: int
    low_findings: int
    info_findings: int
