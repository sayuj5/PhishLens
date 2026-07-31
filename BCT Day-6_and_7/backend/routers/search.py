from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from backend import models, schemas
from backend.database import get_db
from .users import oauth2_scheme

router = APIRouter(prefix="/api/search", tags=["search"], dependencies=[Depends(oauth2_scheme)])

@router.get("/", response_model=schemas.SearchResult)
def global_search(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    search_term = f"%{q}%"
    
    # Search Assets (hostname, ip, mac, vendor, os)
    assets = db.query(models.Asset).filter(
        or_(
            models.Asset.hostname.ilike(search_term),
            models.Asset.ip_address.ilike(search_term),
            models.Asset.mac_address.ilike(search_term),
            models.Asset.vendor.ilike(search_term),
            models.Asset.os.ilike(search_term)
        )
    ).limit(20).all()
    
    # Search Networks (cidr, name, description)
    networks = db.query(models.Network).filter(
        or_(
            models.Network.cidr.ilike(search_term),
            models.Network.name.ilike(search_term),
            models.Network.description.ilike(search_term)
        )
    ).limit(10).all()
    
    return schemas.SearchResult(assets=assets, networks=networks)
