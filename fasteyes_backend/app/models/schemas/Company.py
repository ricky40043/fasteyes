# from typing import List
from typing import Optional

from pydantic import BaseModel, EmailStr

# from app.models.domain.item import item
from datetime import datetime


class Base(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CompanyPostViewModel(Base):
    name: str
    description: str

    class Config:
        schema_extra = {
            "example": {
                "name": "123",
                "description": "ricky4004",
            }
        }


class CompanyViewModel(Base):
    id: str
    name: str
    description: str
    user_id: int
    created_at: datetime
    updated_at: datetime