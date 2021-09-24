from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class staff(Base):
    __tablename__ = "staffs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    serial_number = Column(String, index=True)
    card_number = Column(String, index=True)
    national_id_number = Column(String, index=True)
    birthday = Column(DateTime, index=True)
    gender = Column(String, index=True)
    telephone_number = Column(String, index=True)
    department = Column(String, index=True)
    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    is_enable = Column(Boolean, index=True, default=True)
    status = Column(Integer, index=True, default=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    company_id = Column(Integer, ForeignKey("companys.id"))

    def __init__(self, email, serial_number, card_number, national_id_number, birthday, name, department_id,
                 telephone_number, gender, company_id, status, *args, **kwargs):
        self.name = name
        self.serial_number = serial_number
        self.card_number = card_number
        self.email = email
        self.status = status
        self.national_id_number = national_id_number
        self.birthday = birthday
        self.gender = gender
        self.telephone_number = telephone_number
        self.department_id = department_id
        self.is_enable = False
        self.company_id = company_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.start_date = datetime.now()
        self.end_date = datetime.now()

    def __repr__(self):
        return 'id={}, email={}, name={},telephone_number={},created_at={}'.format(
            self.id, self.email, self.name, self.telephone_number, self.created_at
        )

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'serial_number': self.serial_number,
            'card_number': self.card_number,
            'telephone_number': self.telephone_number,
            'status': self.status,
            'national_id_number': self.national_id_number,
            'birthday': str(self.birthday),
            'gender': self.gender,
            'department_id': self.department_id,
            'is_enable': self.is_enable,
            'company_id': self.company_id,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }