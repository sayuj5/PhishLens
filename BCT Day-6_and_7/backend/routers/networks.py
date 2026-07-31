from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend import models, schemas
from backend.database import get_db
from .users import oauth2_scheme

router = APIRouter(prefix="/api/networks", tags=["networks"], dependencies=[Depends(oauth2_scheme)])

@router.get("/", response_model=List[schemas.Network])
def read_networks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    networks = db.query(models.Network).offset(skip).limit(limit).all()
    return networks

@router.post("/", response_model=schemas.Network)
def create_network(network: schemas.NetworkCreate, db: Session = Depends(get_db)):
    db_network = models.Network(**network.model_dump())
    db.add(db_network)
    db.commit()
    db.refresh(db_network)
    return db_network
