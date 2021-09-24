from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from app.db.database import Base
from datetime import datetime


class department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    company_id = Column(Integer, ForeignKey("companys.id"))

    def __init__(self, name, description, company_id):
        self.name = name
        self.description = description
        self.company_id = company_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'company_id': self.company_id,
            'description': self.description,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }
