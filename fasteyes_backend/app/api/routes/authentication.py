from datetime import timedelta
from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette import status

from app.Server.device.crud import get_device_by_user_id
from app.Server.send_email import SendEmailVerficationEmail, SendForgetPasswordEmail, send_email_async, \
    send_Verfiy_code_email_async
from app.helper.authentication import Authorize_user
from app.Server.company.crud import get_company_by_user_id, get_department_from_company
from app.Server.authentication import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, \
    checkLevel, Authority_Level, get_tocken, create_random_verify_code, \
    save_verify_code_to_token, check_verify_code
from app.Server.authentication.crud import change_user_level_to_hr, set_user_enable, create_and_set_user_password, \
    clear_all_data
from app.Server.user.crud import check_User_Exist, check_Email_Exist
from app.db.database import get_db

from app.models.schemas.user import LoginResultUserViewModel, UserViewModel, UserLoginViewModel, \
    DeviceLoginResultUserViewModel

router = APIRouter()


# 登入
@router.post("/auth/login", response_model=LoginResultUserViewModel)
async def login(user_data: UserLoginViewModel,
                Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(user_data.email, user_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.verify_code_enable:
        # 產生認證碼 4碼
        verify_code = create_random_verify_code()
        # 儲存認證碼 (做成一個Token 並 Save)
        save_verify_code_to_token(verify_code,user_data.email)
        # 寄信
        await send_Verfiy_code_email_async(user_data.email, verify_code)
        raise HTTPException(
            status_code=202,
            detail="Login step1 Done",
        )

    else:
        access_token = Authorize.create_access_token(subject=user.email, expires_time=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token = Authorize.create_refresh_token(subject=user.email)
        device_list = get_device_by_user_id(db, user.id)
        cmpany_list = get_company_by_user_id(db, user.id)
        deparment_list = []
        for cmpany in cmpany_list:
            department = get_department_from_company(db, cmpany.id)
            deparment_list.extend(department)
        return {"User": user, "Status": user.is_enable, "access_token": access_token,
                "refresh_token": refresh_token, "token_type": "bearer",
                "Devices": device_list, "Company": cmpany_list, "Department": deparment_list}


# device 登入
@router.post("/auth/device-login", response_model=DeviceLoginResultUserViewModel)
async def login(user_data: UserLoginViewModel,
                Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(user_data.email, user_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = Authorize.create_access_token(subject=user.email, expires_time=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    return {"User": user, "access_token": access_token,
            "refresh_token": refresh_token, "token_type": "bearer"}


# 登入 2次驗證 step2
@router.post("/auth/login/verify_code", response_model=LoginResultUserViewModel)
async def login(user_data: UserLoginViewModel,verify_code: str, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(user_data.email, user_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 檢查認證碼
    if not check_verify_code(verify_code,user_data.email):
        raise HTTPException(status_code=401, detail="認證碼錯誤")

    access_token = Authorize.create_access_token(subject=user.email, expires_time=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    device_list = get_device_by_user_id(db, user.id)
    cmpany_list = get_company_by_user_id(db, user.id)
    deparment_list = []
    for cmpany in cmpany_list:
        department = get_department_from_company(db, cmpany.id)
        deparment_list.extend(department)
    return {"User": user, "Status": user.is_enable, "access_token": access_token,
            "refresh_token": refresh_token, "token_type": "bearer",
            "Devices": device_list, "Company": cmpany_list, "Department": deparment_list}

# 取得登入User
# @router.get("/auth/user")
# def user(Authorize: AuthJWT = Depends()):
#     Authorize.jwt_required()
#
#     current_user = Authorize.get_jwt_subject()
#     return {"user": current_user}


# 透過email認證身份
@router.get("/auth/verify_email")
def VerifyEmail(token: str, db: Session = Depends(get_db)):
    email = get_tocken(token)

    if not check_Email_Exist(db, email):
        return "Email is not exist"
    # 啟動Userserial_number
    set_user_enable(db, email)
    # 刪除暫存啟動碼

    return email


# 透過email寄信
@router.post("/auth/resend_verification_email")
async def ResendVerificationEmail(email: str, db: Session = Depends(get_db)):
    if not check_Email_Exist(db, email):
        return "Email is not exist"

    await SendEmailVerficationEmail(email)
    return "ResendVerificationEmail Done"


# 忘記密碼寄信
@router.post("/auth/forget_password")
async def ForgetPassword(email: str, db: Session = Depends(get_db)):
    if not check_Email_Exist(db, email):
        return "Email is not exist"

    password = create_and_set_user_password(db, email)

    await SendForgetPasswordEmail(email, password)
    return "SendForgetPasswordEmail Done"


# 改變權限 Admin
@router.patch("/auth/users/{user_id}/change", response_model=UserViewModel)
def UpgradeHRAccount(user_id: int, level: int, db: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    check_User_Exist(db, user_id)

    return change_user_level_to_hr(db, user_id, level)


# 取得登入User
@router.post("/auth/pingServer")
def pingServer(db: Session = Depends(get_db),
               Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize_user(Authorize, db)
    return current_user


# 更新 token
@router.post('/auth/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.delete('/auth/clear_all_data')
def ClearAllData(db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    if not checkLevel(current_user, Authority_Level.RD.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    clear_all_data(db)

    return "Clear Done"
