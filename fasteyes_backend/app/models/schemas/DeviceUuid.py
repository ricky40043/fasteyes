# from typing import List
from typing import Optional

from pydantic import BaseModel, EmailStr

# from app.models.domain.item import item
from datetime import datetime


from app.models.schemas.HardwareUuid import HardwareUuidViewModel


class Base(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class DeviceUuidViewModel(Base):
    id: int
    uuid: str
    creator: str
    created_at: datetime
    updated_at: datetime
    registered_at: Optional[datetime] = None
    is_registered: bool
    is_enable: bool


class HardwareUuid_and_HardwareUuidViewModel(Base):
    DeviceUUID: DeviceUuidViewModel
    HardwareUUID: HardwareUuidViewModel