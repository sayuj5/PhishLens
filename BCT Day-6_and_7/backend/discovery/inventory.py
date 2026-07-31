from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timezone
import json

from backend import models
from backend.logger import discovery_logger

def update_or_create_asset(db: Session, asset_data: dict) -> models.Asset:
    """
    Deduplicates and updates an asset based on IP, MAC, or Hostname.
    """
    ip = asset_data.get("ip_address")
    mac = asset_data.get("mac_address")
    hostname = asset_data.get("hostname")
    
    # 1. Try to find existing asset
    query = db.query(models.Asset)
    filters = []
    if mac:
        filters.append(models.Asset.mac_address == mac)
    if ip:
        filters.append(models.Asset.ip_address == ip)
    if hostname:
        filters.append(models.Asset.hostname == hostname)
        
    existing_asset = None
    if filters:
        existing_asset = query.filter(or_(*filters)).first()
        
    if existing_asset:
        # Update existing
        if ip and not existing_asset.ip_address:
            existing_asset.ip_address = ip
        if mac and not existing_asset.mac_address:
            existing_asset.mac_address = mac
        if hostname and not existing_asset.hostname:
            existing_asset.hostname = hostname
            
        existing_asset.last_seen = datetime.now(timezone.utc)
        existing_asset.is_active = True
        
        discovery_logger.debug(f"Updated existing asset ID {existing_asset.id}")
        asset = existing_asset
    else:
        # Create new
        asset = models.Asset(
            ip_address=ip,
            mac_address=mac,
            hostname=hostname,
            vendor=asset_data.get("vendor"),
            os=asset_data.get("os"),
            is_active=True
        )
        db.add(asset)
        db.flush() # flush to get asset.id
        
        # Log History
        history = models.AssetHistory(
            asset_id=asset.id,
            event_type="created",
            event_data=json.dumps({"ip": ip, "hostname": hostname})
        )
        db.add(history)
        discovery_logger.info(f"Created new asset: {ip or hostname or mac}")
        
    db.commit()
    db.refresh(asset)
    
    # Update Ports and Services if provided
    ports_data = asset_data.get("ports", [])
    for port_info in ports_data:
        update_port_and_service(db, asset.id, port_info)
        
    return asset

def update_port_and_service(db: Session, asset_id: int, port_info: dict):
    port_number = port_info.get("port")
    protocol = port_info.get("protocol", "tcp")
    
    port = db.query(models.Port).filter(
        models.Port.asset_id == asset_id, 
        models.Port.port_number == port_number,
        models.Port.protocol == protocol
    ).first()
    
    if not port:
        port = models.Port(
            asset_id=asset_id,
            port_number=port_number,
            protocol=protocol,
            state="open"
        )
        db.add(port)
        
        # Log History for new port
        history = models.AssetHistory(
            asset_id=asset_id,
            event_type="port_opened",
            event_data=json.dumps({"port": port_number, "protocol": protocol})
        )
        db.add(history)
        
        db.commit()
        db.refresh(port)
        
    # Update service
    service_name = port_info.get("service")
    if service_name:
        service = db.query(models.Service).filter(models.Service.port_id == port.id).first()
        if not service:
            service = models.Service(port_id=port.id, service_name=service_name, version=port_info.get("version"))
            db.add(service)
        elif service.service_name != service_name or service.version != port_info.get("version"):
            # Service changed
            service.service_name = service_name
            service.version = port_info.get("version")
            history = models.AssetHistory(
                asset_id=asset_id,
                event_type="service_changed",
                event_data=json.dumps({"port": port_number, "new_service": service_name, "version": port_info.get("version")})
            )
            db.add(history)
        db.commit()

def log_discovery_result(db: Session, job_id: int, asset_id: int, raw_data: dict):
    result = models.DiscoveryResult(
        job_id=job_id,
        asset_id=asset_id,
        raw_data=json.dumps(raw_data)
    )
    db.add(result)
    db.commit()
