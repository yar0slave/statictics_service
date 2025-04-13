from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


class DeviceService:
    @staticmethod
    def get_devices(db: Session, skip: int = 0, limit: int = 100) -> List[Device]:
        return db.query(Device).offset(skip).limit(limit).all()

    @staticmethod
    def get_device_by_id(db: Session, device_id: int) -> Optional[Device]:
        return db.query(Device).filter(Device.id == device_id).first()

    @staticmethod
    def get_device_by_device_id(db: Session, device_id: str) -> Optional[Device]:
        return db.query(Device).filter(Device.device_id == device_id).first()

    @staticmethod
    def get_devices_by_user_id(db: Session, user_id: int) -> List[Device]:
        return db.query(Device).filter(Device.user_id == user_id).all()

    @staticmethod
    def create_device(db: Session, device: DeviceCreate) -> Device:
        db_device = Device(
            device_id=device.device_id,
            name=device.name,
            user_id=device.user_id
        )
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device

    @staticmethod
    def update_device(db: Session, device_id: int, device_update: DeviceUpdate) -> Optional[Device]:
        db_device = DeviceService.get_device_by_id(db, device_id)
        if not db_device:
            return None

        update_data = device_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_device, key, value)

        db.commit()
        db.refresh(db_device)
        return db_device

    @staticmethod
    def delete_device(db: Session, device_id: int) -> bool:
        db_device = DeviceService.get_device_by_id(db, device_id)
        if not db_device:
            return False

        db.delete(db_device)
        db.commit()
        return True