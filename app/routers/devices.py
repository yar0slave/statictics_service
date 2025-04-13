from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas.device import Device, DeviceCreate, DeviceUpdate
from app.services.device_service import DeviceService

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=List[Device])
def read_devices(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db)
):
    devices = DeviceService.get_devices(db, skip=skip, limit=limit)
    return devices


@router.post("/", response_model=Device, status_code=201)
def create_device(
        device: DeviceCreate,
        db: Session = Depends(get_db)
):
    db_device = DeviceService.get_device_by_device_id(db, device.device_id)
    if db_device:
        raise HTTPException(status_code=400, detail="Device with this ID already exists")

    return DeviceService.create_device(db=db, device=device)


@router.get("/{device_id}", response_model=Device)
def read_device(
        device_id: str = Path(...),
        db: Session = Depends(get_db)
):
    db_device = DeviceService.get_device_by_device_id(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device


@router.put("/{device_id}", response_model=Device)
def update_device(
        device_id: str = Path(...),
        device_update: DeviceUpdate = None,
        db: Session = Depends(get_db)
):
    db_device = DeviceService.get_device_by_device_id(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    updated_device = DeviceService.update_device(
        db=db,
        device_id=db_device.id,
        device_update=device_update
    )

    return updated_device


@router.delete("/{device_id}", status_code=204)
def delete_device(
        device_id: str = Path(...),
        db: Session = Depends(get_db)
):
    db_device = DeviceService.get_device_by_device_id(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    deleted = DeviceService.delete_device(db=db, device_id=db_device.id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete device")