import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.domain.Error_handler import UnicornException
from app.models.domain.HardwareUuid import hardwareUuid
from app.models.schemas.HardwareUuid import HardwareUuidRegistViewModel


def get_all_hardwareUuid(db: Session):
    return db.query(hardwareUuid).all()


def search_hardwareUuid(db: Session, uuid: str):
    HardwareUuid_db = db.query(hardwareUuid).filter(hardwareUuid.uuid == uuid).first()

    if not HardwareUuid_db:
        raise UnicornException(name=search_hardwareUuid.__name__,
                               description="hardware_uuid is not exist", status_code=404)
    return HardwareUuid_db


def create_hardwareUuid(db: Session, current_user_name: str, device_uuid: uuid, product_number: str):
    hardware_uuid = uuid.uuid4()
    # 檢查UUID是否有了
    while True:
        if db.query(hardwareUuid).filter(hardwareUuid.uuid == str(hardware_uuid)).first():
            hardware_uuid = uuid.uuid4()
        else:
            break

    if db.query(hardwareUuid).filter(hardwareUuid.device_uuid == device_uuid).first():
        raise UnicornException(name=create_hardwareUuid.__name__,
                               description="device_uuid is used in other Hardware", status_code=500)

    db.begin()
    try:
        HardwareUuid_db = hardwareUuid(current_user_name, hardware_uuid, device_uuid, product_number)
        db.add(HardwareUuid_db)
        db.commit()
        db.refresh(HardwareUuid_db)
    except Exception as e:
        db.rollback()
        raise UnicornException(name=create_hardwareUuid.__name__, description=str(e), status_code=500)

    return HardwareUuid_db


# def create_hardwareUuids(db: Session, current_user_name: str, DeviceUuidList: list[str], product_number: str):
#     hardware_uuid_List = []
#     for DeviceUuid in DeviceUuidList:
#         hardware_db = create_hardwareUuid(db, current_user_name, DeviceUuid, product_number)
#         hardware_uuid_List.append(hardware_db)
#
#     return hardware_uuid_List


def register_hardwareUuid(db: Session, HardwareUuidSearch: HardwareUuidRegistViewModel):
    HardwareUuid_db_list = db.query(hardwareUuid).all()
    for HardwareUuid_db in HardwareUuid_db_list:
        # print(HardwareUuid_db)
        if HardwareUuid_db.uuid == HardwareUuidSearch.hardware_uuid and \
                hardwareUuid.device_uuid == HardwareUuidSearch.device_uuid:

            db.begin()
            try:
                HardwareUuid_db.is_registered = True
                db.commit()
                db.refresh(HardwareUuid_db)
            except Exception as e:
                db.rollback()
                raise UnicornException(name=register_hardwareUuid.__name__, description=str(e), status_code=500)
    raise UnicornException(name=register_hardwareUuid.__name__, description="HardwareUuid is not exist",
                           status_code=404)


def reset_hardwareUuid(db: Session, uuid: str):
    HardwareUuid_db = db.query(hardwareUuid).filter(hardwareUuid.uuid == uuid).first()
    db.begin()
    try:
        HardwareUuid_db.is_registered = False
        db.commit()
        db.refresh(HardwareUuid_db)
    except Exception as e:
        db.rollback()
        raise UnicornException(name=reset_hardwareUuid.__name__, description=str(e), status_code=500)

    return HardwareUuid_db


def get_hardwareUuid_by_deviceuuid(db: Session, deviceuuid: str):
    # HardwareUuid_list_db = db.query(hardwareUuid).all()
    # for HardwareUuid_db in HardwareUuid_list_db:
    #     if HardwareUuid_db.device_uuid == deviceuuid:
    #         return HardwareUuid_db
    #
    # raise UnicornException(name=search_hardwareUuid.__name__,
    #                        description="device_uuid is used in other Hardware", status_code=404)

    HardwareUuid_db = db.query(hardwareUuid).filter(hardwareUuid.device_uuid == deviceuuid).first()

    if not HardwareUuid_db:
        raise UnicornException(name=search_hardwareUuid.__name__,
                               description="hardware_uuid is not exist", status_code=404)
    return HardwareUuid_db


def change_hardwareUuid(db: Session, id: int, uuid: str):
    HardwareUuid_db = db.query(hardwareUuid).filter(hardwareUuid.id == id).first()
    db.begin()
    try:
        HardwareUuid_db.uuid = uuid
        db.commit()
        db.refresh(HardwareUuid_db)
    except Exception as e:
        db.rollback()
        raise UnicornException(name=reset_hardwareUuid.__name__, description=str(e), status_code=500)

    return HardwareUuid_db
