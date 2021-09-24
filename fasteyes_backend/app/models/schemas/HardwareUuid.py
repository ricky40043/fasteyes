# from typing import List
from typing import Optional

from pydantic import BaseModel, EmailStr

# from app.models.domain.item import item
from datetime import datetime

from pyrsistent import optional

from app.models.schemas.Device import DeviceViewModel, DeviceSettingViewModel


class Base(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True



class HardwareUuidSearchViewModel(Base):
    hardwareuuid: str

    class Config:
        schema_extra = {
            "example": {
                "hardwareuuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            }
        }


class HardwareUuidRegistViewModel(Base):
    hardware_uuid: str
    device_uuid: str

    class Config:
        schema_extra = {
            "example": {
                "hardware_uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "device_uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            }
        }


class HardwareUuidViewModel(Base):
    id: int
    product_number: Optional[str] = []
    uuid: str
    device_uuid: str
    creator: str
    created_at: datetime
    updated_at: datetime
    registered_at: Optional[datetime] = None
    is_enable: bool
    is_registered: bool


class HardwareUuid_and_DeviceViewModel(Base):
    Hardware: HardwareUuidViewModel
    Device: Optional[DeviceViewModel]
    Settings: Optional[DeviceSettingViewModel]
