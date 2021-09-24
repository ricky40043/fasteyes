from sqlalchemy.orm import Session

from app.models.domain.DeviceSetting import deviceSetting
from app.models.domain.Error_handler import UnicornException


def get_device_setting_by_device_id(db: Session, device_id: int):
    return db.query(deviceSetting).filter(deviceSetting.device_id == device_id).first()


def create_device_setting(db: Session, device_id: int):
    db.begin()
    try:
        deviceSetting_db = deviceSetting(device_id = device_id)
        db.add(deviceSetting_db)
        db.commit()
        db.refresh(deviceSetting_db)
    except Exception as e:
        db.rollback()
        raise UnicornException(name=create_device_setting.__name__, description=str(e), status_code=500)

    return deviceSetting_db


def delete_device_setting_by_device_id(db: Session, device_id: int):
    deviceSetting_db = db.query(deviceSetting).filter(deviceSetting.device_id == device_id).first()
    if deviceSetting_db:
        db.begin()
        try:
            db.delete(deviceSetting_db)
            db.commit()
        except Exception as e:
            db.rollback()
            raise UnicornException(name=delete_device_setting_by_device_id.__name__, description=str(e), status_code=500)

    return deviceSetting_db