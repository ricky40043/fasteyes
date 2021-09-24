# from typing import List
from typing import Optional

from pydantic import BaseModel, EmailStr

# from app.models.domain.item import item
from datetime import datetime


class Base(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class LoginViewModel(Base):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "password": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            }
        }