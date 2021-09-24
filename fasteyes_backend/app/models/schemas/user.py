# from typing import List
from typing import Optional

from pydantic import BaseModel, EmailStr

# from app.models.domain.item import item
from datetime import datetime


from app.models.schemas.Company import CompanyViewModel
from app.models.schemas.Department import DepartmentViewModel
from app.models.schemas.Device import DeviceViewModel


class UserBase(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserPostViewModel(UserBase):
    email: EmailStr
    password: str
    name: str
    telephone_number: str = ""
    address: str = ""
    country: str = ""
    usage: str = ""
    company_scale: str = ""
    industry: str = ""

    class Config:
        schema_extra = {
            "example": {
                "name": "ricky400430012",
                "password": "ricky400430012",
                "telephone_number": "0987654321",
                "email": "ricky400430012@gmail.com",
                "address": "台北市中山區民權東路一段",
                "usage": "商用",
                "country": "Taiwan",
                "company_scale": "10~50",
                "industry": "軟體業",
            }
        }


class UserPatchIInfoViewModel(UserBase):
    name: str
    telephone_number: str = ""
    address: str = ""
    country: str = ""
    usage: str = ""
    company_scale: str = ""
    industry: str = ""

    class Config:
        schema_extra = {
            "example": {
                "name": "ricky4004",
                "telephone_number": "0987654321",
                "address": "台北市中山區民權東路一段",
                "country": "Taiwan",
                "usage": "商用",
                "company_scale": "10~50",
                "industry": "資訊業",
            }
        }


class UserChangeSettingViewModel(UserBase):
    email_alert: Optional[bool] = -1
    language: Optional[int] = -1

    class Config:
        schema_extra = {
            "example": {
                "email_alert": False,
                "language": 0,
            }
        }


class UserPatchAccountViewModel(UserBase):
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "email": "ricky400430012@fastwise.net",
            }
        }


class UserPatchPasswordViewModel(UserBase):
    new_password: str
    old_password: str

    class Config:
        schema_extra = {
            "example": {
                "new_password": "ricky4004",
                "old_password": "ricky4004"
            }
        }


class UserLoginViewModel(UserBase):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "ricky4004@gmail.com",
                "password": "ricky4004"
            }
        }


class UserViewModel(UserBase):
    id: int
    email: str
    name: str
    address: str = ""
    country: str = ""
    telephone_number: str = ""
    companyScale: str = ""
    usage: str = ""
    industry: str = ""
    created_at: datetime
    updated_at: datetime
    level: int
    email_alert: bool
    language: int


class LoginResultUserViewModel(UserBase):
    User: UserViewModel
    Status: bool
    access_token: str
    refresh_token: str
    token_type: str
    Devices: list[DeviceViewModel]
    Company: list[CompanyViewModel]
    Department: list[DepartmentViewModel]


class DeviceLoginResultUserViewModel(UserBase):
    User: UserViewModel
    access_token: str
    refresh_token: str
    token_type: str
