from datetime import datetime
from typing import Dict, List, Optional

import cv2
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from app.helper.authentication import Authorize_user
from app.helper.device import check_Device_Authority
from app.helper.observation import check_observation_Authority
from app.helper.staff import check_Staff_Authority
from app.Server.authentication import checkLevel, Authority_Level
from app.Server.device.crud import get_device_by_device_id
from app.Server.observation.crud import update_observation, delete_observation_by_id, \
    delete_all_observation_by_device_id, get_Observations_by_device_id_and_staff_id, get_Observations_by_staff_id, \
    get_Observations_by_device_id_and_timespan
from app.Server.observation_file.crud import delete_observation_image_by_id, delete_all_observation_image_by_device_id, \
    upload_observation_image, download_observation_image
from app.db.database import get_db
from app.models.schemas.Observation import ObservationViewModel, ObservationPatchViewModel

router = APIRouter()


# 裝置ID 員工ID 取得所有觀測 (HRAccess)
@router.get("/device/{device_id}/observations/staff/{staff_id}", response_model=List[ObservationViewModel])
def GetObservationsByDeviceId_And_StaffId(device_id: int,
                                          staff_id: int,
                                          db: Session = Depends(get_db),
                                          Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Device_Authority(db, current_user, device_id)

    return get_Observations_by_device_id_and_staff_id(db, device_id, staff_id)


# 員工ID 取得所有觀測 (HRAccess)
@router.get("/observations/staff/{staff_id}", response_model=List[ObservationViewModel])
def GetObservationsByDeviceId_And_StaffId(staff_id: int,
                                          start_timestamp: Optional[datetime] = None,
                                          end_timestamp: Optional[datetime] = None,
                                          db: Session = Depends(get_db),
                                          Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Staff_Authority(db, current_user, staff_id)
    if start_timestamp and end_timestamp:
        return get_Observations_by_device_id_and_timespan(db, staff_id, start_timestamp, end_timestamp)
    else:
        return get_Observations_by_staff_id(db, staff_id)


# 觀測ID 取得觀測 (HRAccess)
@router.patch("/observations/{observation_id}", response_model=ObservationViewModel)
def UpdateObservation(observation_id: int, obsPatch: ObservationPatchViewModel,
                      db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    check_observation_Authority(db, current_user, observation_id)

    return update_observation(db, observation_id, obsPatch)


# 觀測ID 刪除觀測 (HRAccess)
@router.delete("/observations/{observation_id}", response_model=ObservationViewModel)
def DeleteObservation(observation_id: int,
                      db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    check_observation_Authority(db, current_user, observation_id)

    delete_observation_image_by_id(db, observation_id)

    return delete_observation_by_id(db, observation_id)


# 裝置ID file_name 上傳觀測image (HRAccess)
@router.post("/Files/upload/image/device/{device_id}/file_name/{file_name}")
def Upload_observation_image(device_id: int,
                             file_name: str,
                             image_file: UploadFile = File(...),
                             db: Session = Depends(get_db),
                             Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Device_Authority(db, current_user, device_id)
    return upload_observation_image(db, device_id, file_name, image_file)


# 裝置ID file_name 下載觀測image (HRAccess)
@router.get("/Files/download/image/device/{device_id}/file_name/{file_name}")
def Download_observation_image(device_id: int,
                               file_name: str,
                               db: Session = Depends(get_db)):
                               # Authorize: AuthJWT = Depends()):
    # current_user = Authorize_user(Authorize, db)
    # if not checkLevel(current_user, Authority_Level.Admin.value):
    #     raise HTTPException(status_code=401, detail="權限不夠")

    return download_observation_image(device_id, file_name)


########################################################################################################################

# 觀測ID 刪除所有觀測 (Admin)
@router.delete("/observations/device/{device_id}")
def DeleteAllObservation_by_Device_id(device_id: int,
                                      db: Session = Depends(get_db),
                                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    if get_device_by_device_id(db, device_id) is None:
        raise HTTPException(status_code=404, detail="device is not exist")

    delete_all_observation_image_by_device_id(device_id)
    return delete_all_observation_by_device_id(db, device_id)


# 觀測ID 刪除image (Admin)
@router.delete("/Files/image/observation/{observation_id}")
def delete_observation_image(observation_id: int,
                             db: Session = Depends(get_db),
                             Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    return delete_observation_image_by_id(db, observation_id)


# 裝置ID 刪除所有image (Admin)
@router.delete("/Files/image/device/{device_id}")
def Delete_All_Observation_by_Device_id(device_id: int,
                                        db: Session = Depends(get_db),
                                        Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    if get_device_by_device_id(db, device_id) is None:
        raise HTTPException(status_code=404, detail="device is not exist")

    return delete_all_observation_image_by_device_id(db, device_id)
