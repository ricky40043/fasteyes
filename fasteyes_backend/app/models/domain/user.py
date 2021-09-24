from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

from sqlalchemy.types import TypeDecorator, CHAR
import uuid


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class user(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String, index=True)
    address = Column(String, index=True)
    country = Column(String, index=True)
    telephone_number = Column(String, index=True)
    company_scale = Column(String, index=True)
    usage = Column(String, index=True)
    industry = Column(String, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    is_enable = Column(Boolean, index=True, default=True)
    level = Column(Integer, index=True, default=-1)
    email_alert = Column(Boolean, index=True)
    language = Column(Integer, index=True)
    verify_code_enable = Column(Boolean, index=True)

    def __init__(self, email, password, name, address, country, telephone_number, usage,
                 company_scale, industry,level, **kwargs):
        self.email = email
        self.password = password
        self.name = name
        self.address = address
        self.country = country
        self.telephone_number = telephone_number
        self.usage = usage
        self.is_enable = False
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.serial_number = ""
        self.card_number = ""
        self.company_scale = company_scale
        self.industry = industry
        self.email_alert = False
        self.language = 0
        self.level = level
        self.verify_code_enable = False

    def __repr__(self):
        return 'id={}, email={}, name={},address={},country={},created_at={}'.format(
            self.id, self.email, self.name, self.address, self.country, self.created_at
        )

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'address': self.address,
            'country': self.country,
            'telephone_number': self.telephone_number,
            'usage': self.usage,
            'is_enable': self.is_enable,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'serial_number': self.serial_number,
            'industry': self.industry,
            'company_scale': self.company_scale,
            'email_alert': self.email_alert,
            'language': self.language
        }
