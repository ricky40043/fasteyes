# from typing import List
from typing import Optional

from pydantic import BaseModel, EmailStr

# from app.models.domain.item import item
from datetime import datetime


class UserBase(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ObservationPostViewModel(UserBase):
    result: bool
    phenomenon_time: datetime
    wear_mask: bool
    temperature: float
    staff_id: Optional[int] = -1
    image_name: Optional[str] = ""
    threshold_temperature: float
    compensate_temperature: float
    image_name: str

    class Config:
        schema_extra = {
            "example": {
                "result": True,
                "phenomenon_time": "1994-05-27T00:00",
                "detetect_mask": False,
                "temperature": 37.3,
                "threshold_temperature": 37.5,
                "compensate_temperature": 0,
                "staff_id": 5,
                "image_name": "image_name"
            }
        }


class ObservationViewModel(UserBase):
    id: int
    phenomenon_time: datetime
    created_at: datetime
    updated_at: datetime
    result: bool
    wear_mask: bool
    temperature: float
    device_id: int
    staff_id: Optional[int] = None
    image_name: str
    threshold_temperature: float
    compensate_temperature: float


class ObservationPatchViewModel(UserBase):
    staff_id: int

    class Config:
        schema_extra = {
            "example": {
                "staff_id": 3
            }
        }
