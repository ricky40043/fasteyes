from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey


from app.db.database import Base
from app.models.domain.user import GUID


class deviceUuid(Base):
    __tablename__ = "deviceUuids"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(Text, unique=True)
    creator = Column(String, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    registered_at = Column(DateTime, index=True)
    is_registered = Column(Boolean, index=True)
    is_enable = Column(Boolean, index=True)

    def __init__(self, creator, uuid):

        self.uuid = str(uuid)
        self.creator = creator
        self.is_enable = True
        self.is_registered = False
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __repr__(self):
        return 'id={}, uuid={}, creator={},created_at={},updated_at={},is_registered={} '.format(
            self.id, self.uuid, self.creator, self.created_at, self.updated_at, self.is_registered
        )

    def to_dict(self):
        return {
                "id": self.id,
                "uuid": self.uuid,
                "creator": self.creator,
                "is_registered": self.is_registered,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_enable": self.is_enable
            }

