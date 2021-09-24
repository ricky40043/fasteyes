# from typing import List
from typing import Optional

from pydantic import BaseModel, EmailStr

# from app.models.domain.item import item
from datetime import datetime



class Base(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class DevicePatchInfoViewModel(Base):
    name: str
    description: str

    class Config:
        schema_extra = {
            "example": {
                "name": "ricky4004",
                "description": "string"
            }
        }


class DeviceSettingPatchViewModel(Base):
    uploadScreenshot: Optional[int] = -1
    body_temperature_threshold: Optional[float] = -1

    class Config:
        schema_extra = {
            "example": {
                "uploadScreenshot": "1",
                "body_temperature_threshold": "37.5",
            }
        }


class DevicePatchUserIdViewModel(Base):
    user_id: str

    class Config:
        schema_extra = {
            "example": {
                "user_id": "456",
            }
        }


class DevicePostViewModel(Base):
    user_id: int
    name: str
    description: str
    device_uuid: str

    class Config:
        schema_extra = {
            "example": {
                "user_id": "1",
                "name": "ricky4004",
                "description": "string",
                "device_uuid": "b61fc353-54ba-463c-aab7-0687f705b419"
            }
        }


class DeviceSettingViewModel(Base):
    id: int
    device_id: int
    created_at: datetime
    updated_at: datetime
    email_alert: bool
    body_temperature_threshold: float
    uploadScreenshot: int


class DeviceViewModel(Base):
    id: int
    device_uuid: str
    name: str
    description: str = ""
    user_id: int
    registered_at: datetime
    created_at: datetime
    updated_at: datetime
    Setting: Optional[DeviceSettingViewModel]

# class Device_and_Setting_ViewModel(UserBase):
#     Device: DeviceViewModel
#     Setting: DeviceSettingViewModel
