from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Table, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

asset_tags = Table(
    'asset_tags', Base.metadata,
    Column('asset_id', Integer, ForeignKey('assets.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user") # admin, analyst
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Network(Base):
    __tablename__ = "networks"
    id = Column(Integer, primary_key=True, index=True)
    cidr = Column(String, unique=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    assets = relationship("Asset", back_populates="network")

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True, nullable=True)
    mac_address = Column(String, index=True, nullable=True)
    hostname = Column(String, index=True, nullable=True)
    vendor = Column(String, nullable=True)
    os = Column(String, nullable=True)
    network_id = Column(Integer, ForeignKey("networks.id"), nullable=True)
    risk_score = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    network = relationship("Network", back_populates="assets")
    ports = relationship("Port", back_populates="asset", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=asset_tags, back_populates="assets")
    notes = relationship("AssetNote", back_populates="asset")
    history = relationship("AssetHistory", back_populates="asset")

class Port(Base):
    __tablename__ = "ports"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    port_number = Column(Integer, index=True)
    protocol = Column(String, default="tcp")
    state = Column(String, default="open") # open, closed, filtered
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    
    asset = relationship("Asset", back_populates="ports")
    service = relationship("Service", back_populates="port", uselist=False, cascade="all, delete-orphan")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    port_id = Column(Integer, ForeignKey("ports.id"), unique=True)
    service_name = Column(String, index=True)
    banner = Column(String, nullable=True)
    version = Column(String, nullable=True)
    
    port = relationship("Port", back_populates="service")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    color = Column(String, default="#3b82f6") # Tailwind blue-500
    
    assets = relationship("Asset", secondary=asset_tags, back_populates="tags")

class ScanScope(Base):
    __tablename__ = "scan_scopes"
    id = Column(Integer, primary_key=True, index=True)
    target = Column(String, unique=True, index=True) # e.g. 192.168.1.0/24 or 10.0.0.1
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class ScanProfile(Base):
    __tablename__ = "scan_profiles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    concurrency = Column(Integer, default=100)
    timeout_ms = Column(Integer, default=2000)
    ports = Column(String, default="top_100") # "top_100", "top_1000", "all", or "22,80,443"
    retry_count = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    jobs = relationship("DiscoveryJob", back_populates="profile")

class DiscoveryJob(Base):
    __tablename__ = "discovery_jobs"
    id = Column(Integer, primary_key=True, index=True)
    job_type = Column(String) # quick, full, network
    target = Column(String) # cidr or ip
    status = Column(String, default="pending") # pending, running, completed, failed
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    profile_id = Column(Integer, ForeignKey("scan_profiles.id"), nullable=True)
    
    results = relationship("DiscoveryResult", back_populates="job")
    profile = relationship("ScanProfile", back_populates="jobs")

class DiscoveryResult(Base):
    __tablename__ = "discovery_results"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("discovery_jobs.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    raw_data = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    job = relationship("DiscoveryJob", back_populates="results")

class AssetNote(Base):
    __tablename__ = "asset_notes"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    asset = relationship("Asset", back_populates="notes")

class AssetHistory(Base):
    __tablename__ = "asset_history"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    event_type = Column(String) # created, port_opened, service_changed
    event_data = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    asset = relationship("Asset", back_populates="history")

# ─────────────────────────────────────────────────────────
# Phase 4 – Vulnerability Assessment Framework
# ─────────────────────────────────────────────────────────

class AssessmentPolicy(Base):
    __tablename__ = "assessment_policies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    enabled_categories = Column(Text, default="[]")
    plugin_ids = Column(Text, default="[]")
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    assessment_jobs = relationship("AssessmentJob", back_populates="policy")

class Plugin(Base):
    __tablename__ = "plugins"
    id = Column(Integer, primary_key=True, index=True)
    plugin_id = Column(String, unique=True, index=True)
    name = Column(String)
    version = Column(String, default="1.0.0")
    author = Column(String, default="BlackFalcon")
    category = Column(String, index=True)
    description = Column(String, nullable=True)
    is_enabled = Column(Boolean, default=True)
    config = Column(Text, default="{}")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    findings = relationship("Finding", back_populates="plugin")

class AssessmentJob(Base):
    __tablename__ = "assessment_jobs"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending", index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    policy_id = Column(Integer, ForeignKey("assessment_policies.id"), nullable=True)
    triggered_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    findings_count = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)
    info_count = Column(Integer, default=0)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    asset = relationship("Asset")
    policy = relationship("AssessmentPolicy", back_populates="assessment_jobs")
    findings = relationship("Finding", back_populates="job", cascade="all, delete-orphan")

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("assessment_jobs.id"), nullable=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), index=True)
    plugin_id = Column(Integer, ForeignKey("plugins.id"), nullable=True)
    plugin_ref = Column(String, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    severity = Column(String, index=True)
    category = Column(String, index=True)
    evidence = Column(Text, nullable=True)
    remediation = Column(Text, nullable=True)
    references = Column(Text, default="[]")
    status = Column(String, default="open", index=True)
    risk_score = Column(Float, default=0.0)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    asset = relationship("Asset")
    plugin = relationship("Plugin", back_populates="findings")
    job = relationship("AssessmentJob", back_populates="findings")
    history = relationship("FindingHistory", back_populates="finding", cascade="all, delete-orphan")

class FindingHistory(Base):
    __tablename__ = "finding_history"
    id = Column(Integer, primary_key=True, index=True)
    finding_id = Column(Integer, ForeignKey("findings.id"), index=True)
    previous_status = Column(String, nullable=True)
    new_status = Column(String)
    note = Column(Text, nullable=True)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    finding = relationship("Finding", back_populates="history")

class RiskScore(Base):
    __tablename__ = "risk_scores"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), index=True)
    score = Column(Float)
    critical = Column(Integer, default=0)
    high = Column(Integer, default=0)
    medium = Column(Integer, default=0)
    low = Column(Integer, default=0)
    info = Column(Integer, default=0)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    asset = relationship("Asset")
