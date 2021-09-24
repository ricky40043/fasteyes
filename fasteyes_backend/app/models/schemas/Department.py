from typing import Optional

from pydantic import BaseModel, EmailStr

from datetime import datetime

from app.models.schemas.Staff import StaffViewModel


class Base(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class DepartmentPostViewModel(Base):
    name: str
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "123",
                "description": "ricky4004",
            }
        }


class DepartmentPatchViewModel(Base):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "name": "123",
                "description": "ricky4004",
            }
        }


class DepartmentViewModel(Base):
    id: str
    name: str
    description: str
    company_id: int
    created_at: datetime
    updated_at: datetime


class Department_staffViewModel(Base):
    id: str
    name: str
    description: str
    company_id: int
    created_at: datetime
    updated_at: datetime
    member: list[StaffViewModel]
