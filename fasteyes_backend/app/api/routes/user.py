from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.Server.device.crud import get_device_by_user_id
from app.Server.socket import sio, send_data
from app.helper.authentication import Authorize_user
from app.helper.user import ckeck_user_owner
from app.Server.authentication import Authority_Level, checkLevel, verify_password
from app.Server.user.crud import get_All_users, get_user_by_id, \
    get_companies_by_user_id, get_staffs_By_User_Id, \
    modefy_User, modefy_User_Password, check_Email_Exist, \
    update_UserStatus, update_UserAccount, \
    Create_User, \
    create_Company_From_User, \
    delete_user_By_User_Id, get_user_by_email, get_user_by_name, check_company_name, check_User_Exist, \
    change_user_setting, update_User_Verify_code_enable
from app.db.database import get_db
from app.models.schemas.Company import CompanyViewModel, CompanyPostViewModel
from app.models.schemas.Device import DeviceViewModel
from app.models.schemas.Staff import StaffViewModel
from app.models.schemas.user import UserViewModel, \
    UserPatchPasswordViewModel, UserPatchAccountViewModel, UserPostViewModel, UserChangeSettingViewModel, \
    UserPatchIInfoViewModel

from typing import List

router = APIRouter()


# 取得所有User (Admin)
@router.get("/users/GetAllUsers", response_model=List[UserViewModel])
def GetAllUsers(db: Session = Depends(get_db),
                Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    return get_All_users(db)


# User ID 取得User (HRAccess)
@router.get("/users/{user_id}", response_model=UserViewModel)
def GetUserById(user_id: int, db: Session = Depends(get_db),
                Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    ckeck_user_owner(db, current_user, user_id)

    return get_user_by_id(db, user_id)


# User ID 取得所有devices (Admin)
@router.get("/users/{user_id}/devices", response_model=List[DeviceViewModel])
def GetDeviceByUserId(user_id: int, db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    ckeck_user_owner(db, current_user, user_id)

    return get_device_by_user_id(db, user_id)


# check Email
@router.get("/users/email/exists")
def UserExists(email: str, db: Session = Depends(get_db)):
    if check_Email_Exist(db, email):
        return "Email is exist"


# user id 取得 所有公司 (HRAccess)
@router.get("/users/{user_id}/companies", response_model=List[CompanyViewModel])
def GetCompaniesByUserId(user_id: int, db: Session = Depends(get_db),
                         Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    ckeck_user_owner(db, current_user, user_id)

    return get_companies_by_user_id(db, user_id)


# user id 取得 所有員工 (HRAccess)
@router.get("/users/{user_id}/staffs", response_model=List[StaffViewModel])
def GetStaffsByUserId(user_id: int, db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    ckeck_user_owner(db, current_user, user_id)

    return get_staffs_By_User_Id(db, user_id)


# user id 修改 User Info(HRAccess)
@router.patch("/users/{user_id}/info", response_model=UserViewModel)
def PatchUserInfo(user_id: int, userPatch: UserPatchIInfoViewModel,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    user_db = ckeck_user_owner(db, current_user, user_id)

    return modefy_User(db, user_db, userPatch)


# user id 修改 User setting (HRAccess)
@router.patch("/users/{user_id}/setting", response_model=UserViewModel)
def PatchUserSetting(user_id: int, userPatch: UserChangeSettingViewModel,
                     db: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    user_db = ckeck_user_owner(db, current_user, user_id)

    return change_user_setting(db, user_db, userPatch)


# user id 修改 密碼 (HRAccess)
@router.patch("/users/{user_id}/password", response_model=UserViewModel)
def PatchUserPassword(user_id: int, userPatch: UserPatchPasswordViewModel, db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    user_db = ckeck_user_owner(db, current_user, user_id)

    if not verify_password(userPatch.old_password, user_db.password):
        raise HTTPException(status_code=401, detail="舊密碼錯誤")

    return modefy_User_Password(db, user_id, userPatch)


# 啟用 user (Admin)
@router.patch("/users/{user_id}/is_enable", response_model=UserViewModel)
def UpdateUserStatus(user_id: int, status: bool, db: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_User_Exist(db, user_id)
    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")
    return update_UserStatus(db, user_id, status)


# 啟用二次驗證 user (Admin)
@router.patch("/users/{user_id}/verify_code_enable", response_model=UserViewModel)
def UpdateUserStatus(user_id: int, verify_code_enable: bool, db: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    check_User_Exist(db, user_id)

    return update_User_Verify_code_enable(db, user_id, verify_code_enable)


# # 啟用 user (HRAccess)
# @router.patch("/users/{user_id}/account", response_model=UserViewModel)
# def UpdateUserAccount(user_id: int, userPatch: UserPatchAccountViewModel,
#                       db: Session = Depends(get_db),
#                       Authorize: AuthJWT = Depends()):
#     current_user = Authorize_user(Authorize, db)
#
#     ckeck_user_owner(db, current_user, user_id)
#
#     if get_user_by_email(db, userPatch.email):
#         raise HTTPException(status_code=400, detail="Email already registered")
#
#     return update_UserAccount(db, user_id, userPatch)


# @router.patch("/users/email/account")
# def UpdateUserAccountByEmail(user_email: str, userPatch: UserPatchAccountViewModel,
#                              db: Session = Depends(get_db),
#                              Authorize: AuthJWT = Depends()):
#     Authorize_user(Authorize, db)
#     check_Email_Exist(db, user_email)
#     if get_user_by_email(db, userPatch.email):
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return update_UserAccount_By_Email(db, user_email, userPatch)


# @router.put("/users/email/{user_email}/maximum_joined_group_number", response_model=UserViewModel)
# def PatchUserMaximumJoinedGroupNumberByEmail(user_email: EmailStr, max_number: int, db: Session = Depends(get_db),
#                                              Authorize: AuthJWT = Depends()):
#     current_user = Authorize_user(Authorize, db)
#
#     check_Email_Exist(db, user_email)
#
#     if not checkLevel(current_user, Authority_Level.Admin.value):
#         raise HTTPException(status_code=401, detail="權限不夠")
#
#     return modefy_User_MaximumJoinedGroupNumber_By_Email(db, user_email, max_number)

# 創建 User (Admin)
@router.post("/users", response_model=UserViewModel)
def CreateUser(user_create: UserPostViewModel, db: Session = Depends(get_db),
               Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    if get_user_by_email(db, email=user_create.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if get_user_by_name(db, name=user_create.name):
        raise HTTPException(status_code=400, detail="Name already exist")

    user_db = Create_User(db, user_create)
    return user_db


# 創建公司 (HRAccess)
@router.post("/users/{user_id}/companies", response_model=CompanyViewModel)
def CreateCompanyFromUser(user_id: int, company: CompanyPostViewModel, db: Session = Depends(get_db),
                          Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    ckeck_user_owner(db, current_user, user_id)
    check_company_name(db, user_id, company.name)
    return create_Company_From_User(db, user_id, company)


# 刪除user (Admin)
@router.delete("/users/{user_id}", response_model=UserViewModel)
def DeleteUser(user_id: int, db: Session = Depends(get_db),
               Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    delete_user = get_user_by_id(db, user_id)

    if not delete_user:
        raise HTTPException(status_code=400, detail="user 不存在")

    # 不可以刪除跟你同等或比你高的權限
    if delete_user.level >= current_user.level:
        raise HTTPException(status_code=401, detail="權限不夠")

    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="不可刪除自己")

    return delete_user_By_User_Id(db, user_id)


########################################################################################################################

# 創建 User (Admin)
@router.post("/Adminusers", response_model=UserViewModel)
def CreateAdminUser(user_create: UserPostViewModel, db: Session = Depends(get_db)):

    if get_user_by_email(db, email=user_create.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if get_user_by_name(db, name=user_create.name):
        raise HTTPException(status_code=400, detail="Name already exist")

    user_db = Create_User(db, user_create,level = Authority_Level.RD.value)
    return user_db
