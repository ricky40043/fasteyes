from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.domain.user import GUID


class device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    registered_at = Column(DateTime, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    is_enable = Column(Boolean, index=True)
    device_uuid = Column(Text, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, name, description, user_id, device_uuid, **kwargs):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.device_uuid = str(device_uuid)
        self.is_enable = True
        self.registered_at = datetime.now()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __repr__(self):
        return 'id={}, name={}, description={},registered_at={},updated_at={} '.format(
            self.id, self.name, self.description, self.registered_at, self.updated_at
        )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'registered_at': str(self.registered_at),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'is_enable': self.is_enable,
            'device_uuid': self.device_uuid,
            'user_id': self.user_id
        }
