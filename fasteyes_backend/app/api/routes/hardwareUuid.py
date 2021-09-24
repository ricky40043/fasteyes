from typing import Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.Server.deviceUuid.crud import get_deviceUuid_by_uuid
from app.helper.authentication import Authorize_user
from app.helper.device import check_Device_Authority
from app.Server.device.crud import get_device_by_device_uuid, delete_device_by_id
from app.Server.deviceSetting.crud import get_device_setting_by_device_id, delete_device_setting_by_device_id
from app.Server.hardwareUuid.crud import get_all_hardwareUuid, search_hardwareUuid, create_hardwareUuid, \
    reset_hardwareUuid, change_hardwareUuid
from app.Server.authentication import checkLevel, Authority_Level
from app.Server.observation.crud import delete_observation_by_device_id
from app.db.database import get_db
from app.models.schemas.HardwareUuid import HardwareUuidViewModel, HardwareUuidSearchViewModel, \
    HardwareUuid_and_DeviceViewModel

router = APIRouter()


# 取得所有hardwareUuid (Partner)
@router.get("/hardwareUuids", response_model=List[HardwareUuidViewModel])
def GetHardwareUuidsByCreator(db: Session = Depends(get_db),
                              Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.Partner.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    return get_all_hardwareUuid(db)


# 尋找hardwareUuids (HRAccess)
@router.post("/hardwareUuids/search", response_model=HardwareUuid_and_DeviceViewModel)
def GetDevice_by_hardwareUuid(hardwareUuidpost: HardwareUuidSearchViewModel,
                              db: Session = Depends(get_db),
                              Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.HRAccess.value):
        raise HTTPException(status_code=401, detail="權限不夠")
    hardwareUuid = search_hardwareUuid(db, hardwareUuidpost.hardwareuuid)
    device = get_device_by_device_uuid(db, hardwareUuid.device_uuid)
    if not device:
        return {"Device": None, "Settings": None, "Hardware": hardwareUuid.__dict__}

    setting = get_device_setting_by_device_id(db, device.id)
    if not setting:
        return {"Device": device.__dict__, "Settings": None, "Hardware": hardwareUuid.__dict__}

    return {"Device": device.__dict__, "Settings": setting.__dict__, "Hardware": hardwareUuid.__dict__}


# create
# @router.post("/hardwareUuid", response_model=HardwareUuidViewModel)
# def CreateHardwareUuid(DeviceUuid: str,
#                        db: Session = Depends(get_db),
#                        Authorize: AuthJWT = Depends()):
#     current_user = Authorize_user(Authorize, db)
#     if not checkLevel(current_user, Authority_Level.Partner.value):
#         raise HTTPException(status_code=401, detail="權限不夠")
#
#     if not get_deviceUuid_by_uuid(db,DeviceUuid):
#         raise HTTPException(status_code=404, detail="deviceuuid is not exist")
#
#     return create_hardwareUuid(db, current_user.name, DeviceUuid)
#
#
# @router.post("/hardwareUuids", response_model=List[HardwareUuidViewModel])
# def CreateHardwareUuids(DeviceUuidList: List[str], db: Session = Depends(get_db),
#                         Authorize: AuthJWT = Depends()):
#     current_user = Authorize_user(Authorize, db)
#     if not checkLevel(current_user, Authority_Level.Admin.value):
#         raise HTTPException(status_code=401, detail="權限不夠")
#
#     for DeviceUuid in DeviceUuidList:
#         if not get_deviceUuid_by_uuid(db, DeviceUuid):
#             raise HTTPException(status_code=404, detail="DeviceUuid: "+str(DeviceUuid)+" is not exist")
#
#     return create_hardwareUuids(db, current_user.name, DeviceUuidList)


# @router.post("/hardwareUuids/Register", response_model=HardwareUuidViewModel)
# def RegisterHardwareUuid(hardwareUuidpost: HardwareUuidRegistViewModel,
#                          db: Session = Depends(get_db),
#                          current_user: user = Depends(get_current_active_user)):
#     if not CheckLevel(db, current_user, Authority_Level.User.value):
#         raise HTTPException(status_code=401, detail="權限不夠")
#
#     if not search_hardwareUuid(db, hardwareUuidpost.hardware_uuid):
#         raise HTTPException(status_code=404, detail="HardwareUuids is not exist")
#
#     return register_hardwareUuid(db, hardwareUuidpost)


# hardwareUuid Reset 同時刪除裝置 (Admin)
@router.patch("/hardwareUuids/Reset/{hardwareUuid}", response_model=HardwareUuidViewModel)
def ResetHardwareUuid(hardwareUuid: str,
                      db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    hardware_uuid_db = search_hardwareUuid(db, hardwareUuid)

    if not hardware_uuid_db:
        raise HTTPException(status_code=400, detail="hardware_uuid is not exist")

    if not hardware_uuid_db.is_registered:
        raise HTTPException(status_code=400, detail="hardware_uuid is not registered")

    # Delete Device
    device_db = get_device_by_device_uuid(db, hardware_uuid_db.device_uuid)
    if device_db:
        check_Device_Authority(db, current_user, device_db.id)  # Authority_Level.Device.value
        delete_observation_by_device_id(db, device_db.id)
        delete_device_setting_by_device_id(db, device_db.id)
        delete_device_by_id(db, device_db.id)

    return reset_hardwareUuid(db, hardwareUuid)


###########################################################################################################

@router.patch("/hardwareUuids/{hardwareUuid_id}", response_model=HardwareUuidViewModel)
def changeHardwareUuid(hardwareUuid_id:int,
                       hardwareUuid: str,
                       db: Session = Depends(get_db),
                       Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.RD.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    return change_hardwareUuid(db, hardwareUuid_id, hardwareUuid)

