import json
from datetime import datetime
from typing import Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from app.Server.send_email import send_email_async, send_email_background, send_email_temperature_alert
from app.Server.socket import send_data
from app.Server.staff.crud import get_staff_by_id
from app.helper.authentication import Authorize_user
from app.helper.device import check_Device_Authority
from app.Server.device.crud import get_all_device, modify_deviceSetting, \
    get_Observations_by_device_id, get_user_by_device_id, modify_deviceInfo, \
    check_device_exist_by_deviceuuid, regist_device, check_deviceuuid_exist, delete_device_by_id, \
    get_device_by_device_id
from app.Server.deviceSetting.crud import create_device_setting, delete_device_setting_by_device_id, \
    get_device_setting_by_device_id
from app.Server.observation.crud import create_observation, delete_observation_by_device_id, \
    get_all_observations_by_device_id
from app.Server.authentication import checkLevel, Authority_Level
from app.db.database import get_db
from app.models.schemas.Device import DeviceViewModel, DevicePatchInfoViewModel, DevicePostViewModel, \
    DeviceSettingPatchViewModel, DeviceSettingViewModel
from app.models.schemas.Observation import ObservationViewModel, ObservationPostViewModel
from app.models.schemas.user import UserViewModel

router = APIRouter()


# 取得所有裝置 (Admin)
@router.get("/devices", response_model=List[DeviceViewModel])
def GetDevices(db: Session = Depends(get_db),
               Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")
    return get_all_device(db)


# 裝置ID 取得裝置 (HRAccess)
@router.get("/devices/{device_id}", response_model=DeviceViewModel)
def GetDeviceById(device_id: int, db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    device = check_Device_Authority(db, current_user, device_id)
    return get_device_by_device_id(db, device_id)


# 裝置ID 取得下時間區間內觀測 (HRAccess)
@router.get("/devices/{device_id}/observations", response_model=List[ObservationViewModel])
def GetObservationsByDeviceId(device_id: int,
                              db: Session = Depends(get_db),
                              start_timestamp: Optional[datetime] = None,
                              end_timestamp: Optional[datetime] = None,
                              Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Device_Authority(db, current_user, device_id)
    return get_Observations_by_device_id(db, device_id, start_timestamp, end_timestamp)


# 裝置ID 取得裝置User (HRAccess)
@router.get("/devices/{device_id}/user", response_model=UserViewModel)
def GetUserByDeviceId(device_id: int, db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Device_Authority(db, current_user, device_id)
    return get_user_by_device_id(db, device_id)


# 裝置ID 修改裝置info (HRAccess)
@router.patch("/devices/{device_id}/info", response_model=DeviceViewModel)
def PatchDeviceInfoAsync(device_id: int, devicePatch: DevicePatchInfoViewModel,
                         db: Session = Depends(get_db),
                         Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Device_Authority(db, current_user, device_id)
    modify_deviceInfo(db, device_id, devicePatch)
    device_db = get_device_by_device_id(db, device_id)
    send_data("updateDeviceSetting", device_db)
    return device_db


# 裝置ID 修改裝置setting 打Socket (HRAccess)
@router.patch("/devices/{device_id}/settings", response_model=DeviceViewModel)
def PatchDeviceSettingsAsync(device_id: int, devicePatch: DeviceSettingPatchViewModel,
                             db: Session = Depends(get_db),
                             Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Device_Authority(db, current_user, device_id)
    modify_deviceSetting(db, device_id, devicePatch)
    device_db = get_device_by_device_id(db, device_id)
    send_data("updateDeviceSetting", device_db)
    return device_db


# 註冊 創建裝置 (HRAccess)
@router.post("/devices", response_model=DeviceViewModel)
def RegistDevice(device_in: DevicePostViewModel,
                 db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    if not checkLevel(current_user, Authority_Level.HRAccess.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    check_deviceuuid_exist(db, device_in.device_uuid)
    check_device_exist_by_deviceuuid(db, device_in.device_uuid)
    device_db = regist_device(db, device_in)
    deviceSetting_db = create_device_setting(db, device_db.id)
    # send_data(device_db.to_dict())
    return get_device_by_device_id(db, device_db.id)


# 裝置ID 上傳觀測 打Socket & 寄信 (HRAccess)
@router.post("/devices/{device_id}/observation", response_model=ObservationViewModel)
def UploadObservation(device_id: int,
                      observation_in: ObservationPostViewModel,
                      background_tasks: BackgroundTasks,
                      db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Device_Authority(db, current_user, device_id)
    observation_db = create_observation(db, observation_in, device_id)

    send_data("uploadobservation", observation_db.to_dict())

    if current_user.email_alert and not observation_db.result:  # 寄信
        send_email_temperature_alert(background_tasks=background_tasks, db=db,
                                     email=current_user.email, observation_db=observation_db)

    return observation_db


# 裝置ID 取得所有觀測 (HRAccess)
@router.get("/devices/{device_id}/all_observations", response_model=List[ObservationViewModel])
def GetObservationsByDeviceId(device_id: int,
                              db: Session = Depends(get_db),
                              Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Device_Authority(db, current_user, device_id)
    return get_all_observations_by_device_id(db, device_id)


# 裝置ID 刪除裝置 觀測 裝置設定 (HRAccess)
@router.delete("/devices/{device_id}", response_model=DeviceViewModel)
def delete_Device_and_setting_and_Observation(device_id: int,
                                              db: Session = Depends(get_db),
                                              Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    check_Device_Authority(db, current_user, device_id)  # Authority_Level.Device.value

    delete_observation_by_device_id(db, device_id)

    delete_device_setting_by_device_id(db, device_id)

    return delete_device_by_id(db, device_id)
