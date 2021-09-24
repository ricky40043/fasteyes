from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey

from app.db.database import Base

from app.models.domain.user import GUID


class hardwareUuid(Base):
    __tablename__ = "hardwareUuids"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(Text, unique=True, nullable=False)
    device_uuid = Column(Text, index=True)
    creator = Column(String, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    registered_at = Column(DateTime, index=True)
    is_registered = Column(Boolean, index=True)
    is_enable = Column(Boolean, index=True)
    product_number = Column(String, index=True)

    def __init__(self, creator,uuid, device_uuid, product_number):
        self.uuid = str(uuid)
        self.device_uuid = str(device_uuid)
        self.creator = creator
        self.product_number = product_number
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_enable = True
        self.is_registered = False

    def __repr__(self):
        return 'id={}, uuid={}, creator={},created_at={},updated_at={},is_registered={},device_uuid={} '.format(
            self.id, self.uuid, self.creator, self.created_at, self.updated_at, self.is_registered, self.device_uuid
        )
