import uuid
from sqlalchemy.orm import Session

from app.models.domain.DeviceUuid import deviceUuid
from app.models.domain.Error_handler import UnicornException


def get_all_deviceUuid(db: Session):
    return db.query(deviceUuid).all()


def get_deviceUuid_by_uuid(db: Session, uuid: str):
    return db.query(deviceUuid).filter(deviceUuid.uuid == uuid).first()


def create_deviceUuid(db: Session, current_user_name: str):
    device_uuid = uuid.uuid4()
    # 檢查UUID是否有了
    while True:
        if db.query(deviceUuid).filter(deviceUuid.uuid == str(device_uuid)).first():
            device_uuid = uuid.uuid4()
        else:
            break
    db.begin()
    try:
        DeviceUuid_db = deviceUuid(current_user_name, device_uuid)
        db.add(DeviceUuid_db)
        db.commit()
        db.refresh(DeviceUuid_db)
    except Exception as e:
        db.rollback()
        raise UnicornException(name=create_deviceUuid.__name__, description=str(e), status_code=500)

    return DeviceUuid_db


def create_deviceUuids(db: Session, current_user_name: str, number: int):
    List_deviced = []
    for _ in range(number):
        DeviceUuid_db = create_deviceUuid(db, current_user_name)
        List_deviced.append(DeviceUuid_db)

    return List_deviced


def modify_IsEnable_deviceUuids(db: Session, uuid: str,
                                status: bool):
    DeviceUuid_db = get_deviceUuid_by_uuid(db, uuid)
    db.begin()
    try:
        DeviceUuid_db.is_enable = status
        db.commit()
        db.refresh(DeviceUuid_db)
    except Exception as e:
        db.rollback()
        raise UnicornException(name=create_deviceUuid.__name__, description=str(e), status_code=500)

    return DeviceUuid_db


def modify_IsRegistered_deviceUuids(db: Session, uuid: str,
                                    status: bool):
    DeviceUuid_db = get_deviceUuid_by_uuid(db, uuid)
    db.begin()
    try:
        DeviceUuid_db.is_registered = status
        db.commit()
        db.refresh(DeviceUuid_db)
    except Exception as e:
        db.rollback()
        raise UnicornException(name=create_deviceUuid.__name__, description=str(e), status_code=500)

    return DeviceUuid_db


def delete_DeviceUuid(db: Session, uuid: str):
    DeviceUuid_db = get_deviceUuid_by_uuid(db, uuid)
    db.begin()
    try:
        db.delete(DeviceUuid_db)
        db.commit()
    except Exception as e:
        db.rollback()
        raise UnicornException(name=create_deviceUuid.__name__, description=str(e), status_code=500)

    return DeviceUuid_db
