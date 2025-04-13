from typing import Optional
from pydantic import BaseModel


class DeviceBase(BaseModel):
    device_id: str
    name: Optional[str] = None
    user_id: Optional[int] = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    user_id: Optional[int] = None


class Device(DeviceBase):
    id: int

    class Config:
        from_attributes = True