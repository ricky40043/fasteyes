from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean, JSON, Float
from app.db.database import Base


class deviceSetting(Base):
    __tablename__ = "device_settings"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    email_alert = Column(Boolean, index=True)
    body_temperature_threshold = Column(Float, index=True)
    uploadScreenshot = Column(Integer, index=True)
    # cheatNumberSwitch = Column(Boolean, index=True)
    # cheatNumber = Column(Integer, index=True)
    # maskDetect = Column(Boolean, index=True)
    # maskDetectVolumn = Column(Boolean, index=True)
    # brightness = Column(Integer, index=True)
    # backlightCompensation = Column(Integer, index=True)
    # FRThreshold = Column(Integer, index=True)
    # volumn = Column(Integer, index=True)

    device_id = Column(Integer, ForeignKey("devices.id"))

    def __init__(self, device_id):
        self.device_id = device_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.body_temperature_threshold = 37.5
        self.uploadScreenshot = 0
        self.email_alert = True

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'email_alert': self.email_alert,
            'body_temperature_threshold': self.body_temperature_threshold,
            'uploadScreenshot': self.uploadScreenshot,
            'device_id': self.device_id,
        }
