# crud
import uuid
from datetime import datetime
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.Server.authentication import Authority_Level
from app.models.domain.Error_handler import UnicornException
from app.models.domain.user import user
from app.models.domain.Staff import staff
from app.models.domain.Device import device
from app.models.domain.DeviceUuid import deviceUuid
from app.models.domain.Company import company
from app.models.schemas.Company import CompanyPostViewModel
from app.models.schemas.Device import DevicePostViewModel
from app.models.schemas.user import UserPatchPasswordViewModel \
    , UserPatchAccountViewModel, UserPostViewModel, UserChangeSettingViewModel, UserPatchIInfoViewModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def get_All_users(db: Session):
    return db.query(user).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(user).filter(user.id == user_id).first()


def get_UserExists(db: Session, user_email: str):
    return db.query(user).filter(user.email == user_email).first()


def get_companies_by_user_id(db: Session, user_id: int):
    return db.query(company).filter(company.user_id == user_id).all()


# 這裡要用Join
def get_staffs_By_User_Id(db: Session, user_id: int):
    company_db = db.query(company).filter(company.user_id == user_id).first()
    if not company_db:
        raise HTTPException(status_code=400, detail="user 底下沒有company")
    return db.query(staff).filter(staff.company_id == company_db.id).all()


def modefy_User(db: Session, user_db: user, userPatch: UserPatchIInfoViewModel):
    db.begin()
    try:
        user_db.name = userPatch.name
        user_db.address = userPatch.address
        user_db.country = userPatch.country
        user_db.telephone_number = userPatch.telephone_number
        user_db.usage = userPatch.usage
        user_db.company_scale = userPatch.company_scale
        user_db.industry = userPatch.industry
        user_db.updated_at = datetime.now()
        db.commit()
        db.refresh(user_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=modefy_User.__name__, description=str(e), status_code=500)
    return user_db


def change_user_setting(db: Session, user_db: user, userPatch: UserChangeSettingViewModel):
    db.begin()
    try:
        if userPatch.language != -1:
            user_db.language = userPatch.language
        if userPatch.email_alert != -1:
            user_db.email_alert = userPatch.email_alert
        user_db.updated_at = datetime.now()
        db.commit()
        db.refresh(user_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=change_user_setting.__name__, description=str(e), status_code=500)
    return user_db


def modefy_User_Password(db: Session, user_id: int, userPatch: UserPatchPasswordViewModel):
    user_db = db.query(user).filter(user.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="user not exist")
    db.begin()
    try:
        hashed_password = get_password_hash(userPatch.new_password)
        user_db.password = hashed_password
        user_db.updated_at = datetime.now()
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=modefy_User_Password.__name__, description=str(e), status_code=500)
    return user_db


def check_Email_Exist(db: Session, email: str):
    user_db = db.query(user).filter(user.email == email).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="Email does not exist")
    return user_db


# def modefy_UserSettings(db: Session, user_id: int, user_setting_options: str):
#     usersetting_db = db.query(Usersetting).filter(Usersetting.user_id == user_id).first()
#     db.begin()
#     try:
#         if usersetting_db is None:
#             New_Usersetting = Usersetting(user_id=user_id,
#                                           setting=user_setting_options)
#             print("add:", New_Usersetting)
#         else:
#             usersetting_db.setting = user_setting_options
#         db.commit()
#         print("commit:", New_Usersetting)
#
#         db.refresh(usersetting_db)
#     except Exception as e:
#         db.rollback()
#         print(str(e))
#         raise UnicornException(name=modefy_UserSettings.__name__, description=str(e), status_code=500)
#     return usersetting_db
#
#
# def update_AllUserSettings(db: Session, user_setting_options: str):
#     usersetting_dbs = db.query(Usersetting).all()
#     db.begin()
#     try:
#         for usersetting_db in usersetting_dbs:
#             usersetting_db.setting = user_setting_options
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         print(str(e))
#         raise UnicornException(name=update_AllUserSettings.__name__, description=str(e), status_code=500)
#     return "Done"
#
#
# def update_UserSettings(db: Session, user_id: int):
#     usersetting_db = db.query(Usersetting).filter(Usersetting.user_id == user_id).first()
#     if usersetting_db is None:
#         raise HTTPException(status_code=404, detail="usersetting not exist")
#     db.begin()
#     try:
#         if usersetting_db is None:
#             New_Usersetting = Usersetting(users_id=user_id,
#                                           setting="default_user_setting_options")
#             db.add(New_Usersetting)
#         else:
#             usersetting_db.setting = "default_user_setting_options"
#         db.commit()
#         db.refresh(usersetting_db)
#     except Exception as e:
#         db.rollback()
#         print(str(e))
#         raise UnicornException(name=update_UserSettings.__name__, description=str(e), status_code=500)
#     return usersetting_db


def update_UserStatus(db: Session, user_id: int, status: bool):
    user_db = db.query(user).filter(user.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="user not exist")
    db.begin()
    try:
        user_db.is_enable = status
        db.commit()
        db.refresh(user_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=update_UserStatus.__name__, description=str(e), status_code=500)
    return user_db


def update_User_Verify_code_enable(db: Session, user_id: int, verify_code_enable: bool):
    user_db = db.query(user).filter(user.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="user not exist")
    db.begin()
    try:
        user_db.verify_code_enable = verify_code_enable
        db.commit()
        db.refresh(user_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=update_UserStatus.__name__, description=str(e), status_code=500)
    return user_db



def update_UserAccount(db: Session, user_id: int, userPatch: UserPatchAccountViewModel):
    user_db = db.query(user).filter(user.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="user not exist")
    db.begin()
    try:
        user_db.email = userPatch.email
        user_db.updated_at = datetime.now()
        db.commit()
        db.refresh(user_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=update_UserAccount.__name__, description=str(e), status_code=500)
    return user_db


# def update_UserAccount_By_Email(db: Session, email: int, userPatch: UserPatchAccountViewModel):
#     user_db = db.query(user).filter(user.email == email).first()
#     db.begin()
#     try:
#         user_db.email = userPatch.email
#         user_db.updated_at = datetime.now()
#         db.commit()
#         db.refresh(user_db)
#     except Exception as e:
#         db.rollback()
#         print(str(e))
#         raise UnicornException(name=update_UserAccount_By_Email.__name__, description=str(e), status_code=500)
#     return user_db


def Create_User(db: Session, user_create: UserPostViewModel, level = Authority_Level.HRAccess.value):
    db.begin()
    try:
        hashed_password = get_password_hash(user_create.password)
        user_create.password = hashed_password
        db_user = user(**user_create.dict(),
                       level =level,
                       is_company=True)
        db.add(db_user)
        # print("add Done")
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=Create_User.__name__, description=str(e), status_code=500)
    return db_user


def verify_DeviceUuid(db: Session, DeviceIn: DevicePostViewModel):
    DeviceUuid_db = db.query(deviceUuid).filter(deviceUuid.uuid == DeviceIn.device_uuid).first()
    if not DeviceUuid_db:
        raise HTTPException(status_code=404, detail="device_uuid not exist")


def Regist_Device(db: Session, DeviceIn: DevicePostViewModel):
    db.begin()
    try:
        db_Device = device(**DeviceIn.dict())
        db.add(db_Device)
        db.commit()
        db.refresh(db_Device)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=Regist_Device.__name__, description=str(e), status_code=500)
    return db_Device


def check_company_name(db: Session, user_id: int, company_name: str):
    if db.query(company).filter(company.user_id == user_id).filter(company.name == company_name).first():
        raise UnicornException(name=check_company_name.__name__,
                               description="Company name is exist in this user",
                               status_code=400)


def create_Company_From_User(db: Session, user_id: int, companyIn: CompanyPostViewModel):
    db.begin()
    try:
        db_company = company(**companyIn.dict(), user_id=user_id)
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=create_Company_From_User.__name__, description=str(e), status_code=500)
    return db_company


def check_User_Exist(db: Session, user_id: int):
    db_user = db.query(user).filter(user.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user is not exist")
    return db_user


def delete_user_By_User_Id(db: Session, user_id: int):
    db.begin()
    try:
        db_user = db.query(user).filter(user.id == user_id).first()
        db.delete(db_user)
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=delete_user_By_User_Id.__name__, description=str(e), status_code=500)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(user).filter(user.email == email).first()


def get_user_by_name(db: Session, name: str):
    return db.query(user).filter(user.name == name).first()

