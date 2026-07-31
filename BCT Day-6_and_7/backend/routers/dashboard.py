from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from backend import models, schemas
from backend.database import get_db
from .users import oauth2_scheme

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"], dependencies=[Depends(oauth2_scheme)])

@router.get("/", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_assets = db.query(models.Asset).count()
    total_networks = db.query(models.Network).count()
    
    online_hosts = db.query(models.Asset).filter(models.Asset.is_active == True).count()
    offline_hosts = total_assets - online_hosts
    
    active_scan_jobs = db.query(models.DiscoveryJob).filter(models.DiscoveryJob.status == "running").count()
    completed_scans = db.query(models.DiscoveryJob).filter(models.DiscoveryJob.status == "completed").count()
    
    # Calculate average risk score safely
    avg_risk = db.query(func.avg(models.Asset.risk_score)).scalar()
    average_risk_score = float(avg_risk) if avg_risk else 0.0

    return schemas.DashboardStats(
        total_assets=total_assets,
        total_networks=total_networks,
        online_hosts=online_hosts,
        offline_hosts=offline_hosts,
        active_scan_jobs=active_scan_jobs,
        completed_scans=completed_scans,
        average_risk_score=average_risk_score
    )
