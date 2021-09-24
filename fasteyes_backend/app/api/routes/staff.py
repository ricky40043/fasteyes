from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.Server.observation.crud import get_default_staff_id
from app.helper.authentication import Authorize_user
from app.helper.staff import check_Staff_Authority, Check_Staff_Authority_SerialNumber
from app.Server.staff.crud import get_staff_face_images, \
    get_staff_face_image_file, modefy_Staff_Info, delete_Staff_by_Staff_id, delete_staff_all_image, \
    delete_staff_image_by_image_name, check_email_exist, upload_face_file, upload_raw_face_feature, \
    download_raw_face_feature, delete_feature, get_staff_by_current_user
from app.db.database import get_db
from app.models.schemas.FaceFeature import FaceViewModel, FaceFeatureViewModel
from app.models.schemas.Staff import StaffViewModel, StaffPostViewModel, StaffPatchViewModel

router = APIRouter()


# 取得所有員工 (HRAccess)
@router.get("/staffs", response_model=List[StaffViewModel])
def GetStaffs(db: Session = Depends(get_db),
              Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    return get_staff_by_current_user(db, current_user)


# 員工編號 取得員工 (HRAccess)
@router.get("/staffs/SerialNumber/{SerialNumber}", response_model=StaffViewModel)
def GetStaffBySerialNumber(SerialNumber: str, db: Session = Depends(get_db),
                           Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    staff = Check_Staff_Authority_SerialNumber(db, current_user, SerialNumber)
    return staff


# 員工ID 取得員工 (HRAccess)
@router.get("/staffs/{staff_id}", response_model=StaffViewModel)
def GetStaffById(staff_id: int, db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    staff = check_Staff_Authority(db, current_user, staff_id)
    return staff


# 員工ID 取得員工臉列表DB (HRAccess)
@router.get("/staffs/{staff_id}/faces/list", response_model=List[FaceViewModel])
def GetStaffFaceImageList(staff_id: int, db: Session = Depends(get_db),
                          Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Staff_Authority(db, current_user, staff_id)
    return get_staff_face_images(db, staff_id)


# 員工ID 取得員工照片 回傳檔案 (HRAccess)
@router.get("/staffs/{staff_id}/faces/{image_name}")
def GetStaffFaceImage(staff_id: int, image_name: str, db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Staff_Authority(db, current_user, staff_id)
    return get_staff_face_image_file(db, staff_id, image_name)


# 員工ID 上傳員工照片 上傳檔案 & 刪除教的資料 (HRAccess)
@router.post("/staffs/{staff_id}/faces", response_model=FaceViewModel)
def AddStaffFaceImagesAsync(staff_id: int, Image_file: UploadFile = File(...), db: Session = Depends(get_db),
                            Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Staff_Authority(db, current_user, staff_id)

    return upload_face_file(db, staff_id, Image_file)


# 員工ID 修改員工資料 (HRAccess)
@router.patch("/staffs/{staff_id}", response_model=StaffViewModel)
def PatchStaffById(staff_id: int, staffPatch: StaffPatchViewModel, db: Session = Depends(get_db),
                   Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Staff_Authority(db, current_user, staff_id)
    return modefy_Staff_Info(db, staff_id, staffPatch)


# 員工ID 刪除員工 (HRAccess)
@router.delete("/staffs/{staff_id}", response_model=StaffViewModel)
def DeleteStaff(staff_id: int, db: Session = Depends(get_db),
                Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Staff_Authority(db, current_user, staff_id)
    delete_staff_all_image(db, staff_id)
    delete_feature(db, staff_id)
    return delete_Staff_by_Staff_id(db, staff_id)


# 員工ID 刪除員工全部照片
@router.delete("/staffs/{staff_id}/all_faces")
def DeleteStaff_faces(staff_id: int, db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Staff_Authority(db, current_user, staff_id)
    return delete_staff_all_image(db, staff_id)


# 員工ID 刪除員工其中一張照片
# @router.delete("/staffs/{staff_id}/faces")
# def DeleteStaffFaceImage(staff_id: int, image_name: str, db: Session = Depends(get_db),
#                          Authorize: AuthJWT = Depends()):
#     current_user = Authorize_user(Authorize, db)
#     check_Staff_Authority(db, current_user, staff_id)
#     get_staff_face_image_file(db, staff_id, image_name)
#     delete_feature(db, staff_id)
#     return delete_staff_image_by_image_name(db, staff_id, image_name)


# 員工ID 上傳員工Feature (HRAccess)
@router.post("/staffs/{staff_id}/raw_face_features")
def Upload_Face_Feature(staff_id: int, feature: str, db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Staff_Authority(db, current_user, staff_id)
    return upload_raw_face_feature(db, staff_id, feature)


# 員工ID 下載員工Feature (HRAccess)
@router.get("/staffs/{staff_id}/raw_face_features", response_model=FaceFeatureViewModel)
def Download_Face_Feature(staff_id: int, db: Session = Depends(get_db),
                          Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Staff_Authority(db, current_user, staff_id)
    return download_raw_face_feature(db, staff_id)


########################################################################################################################
@router.get("/get-default-staff", response_model=StaffViewModel)
def GetDefaultStaff(db: Session = Depends(get_db)):
    staff_db = get_default_staff_id(db)
    return get_default_staff_id(db)
