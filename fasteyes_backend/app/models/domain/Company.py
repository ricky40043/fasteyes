from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey
from app.db.database import Base


class company(Base):
    __tablename__ = "companys"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    is_enable = Column(String, index = True)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self,name,description,user_id,*args, **kwargs):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_enable = True

    def __repr__(self):
        return 'id={}, name={}, description={},created_at={},updated_at={} '.format(
            self.id, self.name, self.description, self.created_at, self.updated_at
        )
