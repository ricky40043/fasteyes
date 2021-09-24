from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey, Float
from app.db.database import Base


class observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True, index=True)
    phenomenon_time = Column(DateTime, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    result = Column(Boolean, index=True)
    wear_mask = Column(Boolean, index=True)
    temperature = Column(Float, index=True)
    threshold_temperature = Column(Float, index=True)
    compensate_temperature = Column(Float, index=True)
    is_enable = Column(Boolean, index=True, default=True)
    image_name = Column(String, index=True)
    staff_id = Column(Integer, ForeignKey("staffs.id"))
    device_id = Column(Integer, ForeignKey("devices.id"))

    def __init__(self, result, device_id, wear_mask, temperature, staff_id,
                 threshold_temperature, compensate_temperature, phenomenon_time, image_name):
        self.phenomenon_time = phenomenon_time
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.result = result
        self.wear_mask = wear_mask
        self.temperature = temperature
        self.image_name = image_name
        self.threshold_temperature = threshold_temperature
        self.compensate_temperature = compensate_temperature
        self.staff_id = staff_id
        self.device_id = device_id
        self.is_enable = True

    # def __repr__(self):
    #     return 'id={}, phenomenon_time={}, result={},wear_mask={},temperature={},staff_id={},image_file_id={},device_id={}'.format(
    #         self.id, self.phenomenon_time, self.result, self.wear_mask, self.temperature, self.staff_id,
    #         self.image_file_id, self.device_id
    #     )

    def to_dict(self):
        return {
            'id': self.id,
            'phenomenon_time': str(self.phenomenon_time),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'result': self.result,
            'wear_mask': self.wear_mask,
            'temperature': self.temperature,
            'threshold_temperature': self.threshold_temperature,
            'compensate_temperature': self.compensate_temperature,
            'is_enable': self.is_enable,
            'image_name': self.image_name,
            'staff_id': self.staff_id,
            'device_id': self.device_id
        }
