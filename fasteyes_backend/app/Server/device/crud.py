from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.Server.deviceSetting.crud import get_device_setting_by_device_id
from app.Server.deviceUuid.crud import get_deviceUuid_by_uuid
from app.Server.hardwareUuid.crud import register_hardwareUuid, search_hardwareUuid, get_hardwareUuid_by_deviceuuid
from app.models.domain.Device import device
from app.models.domain.DeviceSetting import deviceSetting
from app.models.domain.DeviceUuid import deviceUuid
from app.models.domain.Error_handler import UnicornException
from app.models.domain.Observation import observation
from app.models.domain.user import user
from app.models.schemas.Device import DevicePatchInfoViewModel, DevicePostViewModel, \
    DeviceSettingPatchViewModel


def get_device_by_user_id(db: Session, user_id: int):
    device_list = db.query(device).filter(device.user_id == user_id).all()
    outdata = []
    for device_db in device_list:
        device_setting_db = get_device_setting_by_device_id(db, device_db.id)
        data_dict = device_db.to_dict()
        data_dict["Setting"] = device_setting_db.to_dict()
        outdata.append(data_dict)
    return outdata


def get_all_device(db: Session):
    device_list = db.query(device).all()
    outdata = []
    for device_db in device_list:
        device_setting_db = get_device_setting_by_device_id(db, device_db.id)
        data_dict = device_db.to_dict()
        data_dict["Setting"] = device_setting_db.to_dict()
        outdata.append(data_dict)
    return outdata


def check_device_ower(db: Session, company_id: int, user_id: int):
    device_db = db.query(device).filter(device.id == company_id, device.user_id == user_id).first()
    device_setting_db = get_device_setting_by_device_id(db, device_db.id)
    data_dict = device_db.to_dict()
    data_dict["Setting"] = device_setting_db.to_dict()
    return data_dict


def get_device_by_device_id(db: Session, device_id):
    device_db = db.query(device).filter(device.id == device_id).first()
    device_setting_db = get_device_setting_by_device_id(db, device_db.id)
    data_dict = device_db.to_dict()
    data_dict["Setting"] = device_setting_db.to_dict()
    return data_dict


def get_Observations_by_device_id(db: Session, device_id: int,
                                  start_timestamp: datetime,
                                  end_timestamp: datetime):
    return db.query(observation).filter(observation.device_id == device_id,
                                        observation.created_at >= start_timestamp,
                                        observation.created_at <= end_timestamp).all()


def get_user_by_device_id(db: Session, device_id: int):
    device_db = db.query(device).filter(device.id == device_id).first()
    return db.query(user).filter(user.id == device_db.user_id).first()


def modify_deviceInfo(db: Session, device_id: int, devicePatch: DevicePatchInfoViewModel):
    device_db = db.query(device).filter(device.id == device_id).first()
    db.begin()
    try:
        device_db.name = devicePatch.name
        device_db.description = devicePatch.description
        device_db.updated_at = datetime.now()
        db.commit()
        db.refresh(device_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=modify_deviceInfo.__name__, description=str(e), status_code=500)
    return device_db


def modify_deviceSetting(db: Session, device_id: int, devicePatch: DeviceSettingPatchViewModel):
    deviceSetting_db = db.query(deviceSetting).filter(deviceSetting.device_id == device_id).first()

    db.begin()
    try:
        if not devicePatch.uploadScreenshot == -1:
            deviceSetting_db.uploadScreenshot = devicePatch.uploadScreenshot

        if not devicePatch.body_temperature_threshold == -1:
            deviceSetting_db.body_temperature_threshold = devicePatch.body_temperature_threshold

        deviceSetting_db.updated_at = datetime.now()
        db.commit()
        db.refresh(deviceSetting_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=modify_deviceSetting.__name__, description=str(e), status_code=500)
    return deviceSetting_db


def change_device_user_id(db: Session, device_id: int, user_id: int):
    device_db = db.query(device).filter(device.id == device_id).first()
    db.begin()
    try:
        device_db.user_id = user_id
        device_db.updated_at = datetime.now()
        db.commit()
        db.refresh(device_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=change_device_user_id.__name__, description=str(e), status_code=500)
    return device_db


def check_deviceuuid_exist(db: Session, device_uuid: str):
    if not db.query(deviceUuid).filter(deviceUuid.uuid == device_uuid).first():
        raise UnicornException(name=check_deviceuuid_exist.__name__,
                               description="device_uuid is not exist ", status_code=400)


def check_device_exist_by_deviceuuid(db: Session, device_uuid: str):
    Device_db = db.query(device).filter(device.device_uuid ==device_uuid).first()
    if Device_db:
        raise UnicornException(name=check_device_exist_by_deviceuuid.__name__,
                               description="device is registed ", status_code=400)

    return True


def regist_device(db: Session, device_in: DevicePostViewModel):
    db.begin()
    try:
        deviceUuid_db = get_deviceUuid_by_uuid(db, device_in.device_uuid)
        deviceUuid_db.updated_at = datetime.now()
        deviceUuid_db.registered_at = datetime.now()
        deviceUuid_db.is_registered = True

        hardwareUuid_db = get_hardwareUuid_by_deviceuuid(db, device_in.device_uuid)
        hardwareUuid_db.updated_at = datetime.now()
        hardwareUuid_db.registered_at = datetime.now()
        hardwareUuid_db.is_registered = True
        device_db = device(**device_in.__dict__)
        db.add(device_db)
        db.commit()
        db.refresh(device_db)
    except Exception as e:
        db.rollback()
        raise UnicornException(name=regist_device.__name__, description=str(e), status_code=500)
    return device_db


def delete_device_by_id(db: Session, device_id: int):
    device_db = db.query(device).filter(device.id == device_id).first()
    db.begin()
    try:
        db.delete(device_db)
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=delete_device_by_id.__name__, description=str(e), status_code=500)
    return device_db


def get_device_by_device_uuid(db: Session, device_uuid: str):
    Device_list_db = db.query(device).all()
    # print(Device_list_db)
    for Device_db in Device_list_db:
        if Device_db.device_uuid == device_uuid:
            return Device_db
    return None
