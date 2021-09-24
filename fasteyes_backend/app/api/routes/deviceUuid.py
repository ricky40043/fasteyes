from typing import Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.Server.hardwareUuid.crud import create_hardwareUuid
from app.helper.authentication import Authorize_user
from app.Server.deviceUuid.crud import get_deviceUuid_by_uuid, get_all_deviceUuid, create_deviceUuid, \
    create_deviceUuids, modify_IsEnable_deviceUuids, modify_IsRegistered_deviceUuids, delete_DeviceUuid
from app.Server.authentication import checkLevel, Authority_Level
from app.db.database import get_db
from app.models.schemas.DeviceUuid import DeviceUuidViewModel, HardwareUuid_and_HardwareUuidViewModel
from app.models.schemas.HardwareUuid import HardwareUuidViewModel

router = APIRouter()


# 取得所有裝置UUID (Admin)
@router.get("/deviceUuids", response_model=List[DeviceUuidViewModel])
def GetAllDeviceUuids(db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    return get_all_deviceUuid(db)


# 裝置UUID 取得裝置 (Partner)
@router.get("/deviceUuids/{uuid}", response_model=DeviceUuidViewModel)
def GetDeviceUuidByUuid(uuid: str, db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.Partner.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    return get_deviceUuid_by_uuid(db, uuid)


# 新增 裝置UUID (Partner)
@router.post("/deviceUuids", response_model=HardwareUuid_and_HardwareUuidViewModel)
def CreateDeviceUuid(product_number: str,
                     db: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.Partner.value):
        raise HTTPException(status_code=401, detail="權限不夠")
    deviceUuid_db = create_deviceUuid(db, current_user.name)
    hardwareUuid_db = create_hardwareUuid(db, current_user.name, deviceUuid_db.uuid, product_number)
    # print(deviceUuid_db.__dict__)
    # print(hardwareUuid_db.__dict__)
    return {"DeviceUUID": deviceUuid_db.to_dict(), "HardwareUUID": hardwareUuid_db.__dict__}


# # 新增 多個裝置UUID (Partner)
# @router.post("/deviceUuids/{number}", response_model=Union[List[DeviceUuidViewModel], List[HardwareUuidViewModel]])
# def CreateDeviceUuids(number: int, db: Session = Depends(get_db),
#                       Authorize: AuthJWT = Depends()):
#     current_user = Authorize_user(Authorize, db)
#     if not checkLevel(current_user, Authority_Level.Partner.value):
#         raise HTTPException(status_code=401, detail="權限不夠")
#
#     deviceUuid_db_list = create_deviceUuids(db, current_user.name, number)
#     deviceUuid_list = [deviceUuid.uuid for deviceUuid in deviceUuid_db_list]
#     hardwareUuid_list = create_hardwareUuids(db, current_user.name, deviceUuid_list)
#     return deviceUuid_db_list, hardwareUuid_list


# 更改 裝置狀態 (Admin)
@router.patch("/deviceUuids/{uuid}/isenable", response_model=DeviceUuidViewModel)
def PatchDeviceIsEnable(uuid: str, status: bool,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    if not get_deviceUuid_by_uuid(db, uuid):
        raise HTTPException(status_code=400, detail="deviceUuids is not exist")

    return modify_IsEnable_deviceUuids(db, uuid, status)


####################################################################################
# 更改 裝置註冊狀態 (Admin)
@router.patch("/deviceUuids/{uuid}/isregistered", response_model=DeviceUuidViewModel)
def PatchDeviceIsRegistered(uuid: str, status: bool,
                            db: Session = Depends(get_db),
                            Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    if not get_deviceUuid_by_uuid(db, uuid):
        raise HTTPException(status_code=400, detail="deviceUuids is not exist")

    return modify_IsRegistered_deviceUuids(db, uuid, status)


# 刪除 裝置UUID (Admin)
# @router.delete("/deviceUuids/{uuid}", response_model=DeviceUuidViewModel)
# def DeleteDeviceUuid(uuid: str,
#                      db: Session = Depends(get_db),
#                      Authorize: AuthJWT = Depends()):
#     current_user = Authorize_user(Authorize, db)
#     if not checkLevel(current_user, Authority_Level.Admin.value):
#         raise HTTPException(status_code=401, detail="權限不夠")
#
#     deviceUuid = get_deviceUuid_by_uuid(db, uuid)
#
#     if not deviceUuid:
#         raise HTTPException(status_code=400, detail="deviceUuids is not exist")
#
#     if deviceUuid.is_registered:
#         raise HTTPException(status_code=400, detail="deviceUuids is registered")
#
#     return delete_DeviceUuid(db, uuid)
