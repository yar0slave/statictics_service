from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

from app.schemas.device import Device


class UserBase(BaseModel):
    username: str = Field(..., )
    email: EmailStr = Field(..., )


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class User(UserBase):
    id: int = Field(..., )

    class Config:
        from_attributes = True


class UserWithDevices(User):
    devices: List[Device] = Field(default_factory=list, )

    class Config:
        from_attributes = True
