import os
import shutil
from datetime import datetime
from random import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.Server.authentication import create_random_password
from app.Server.user.crud import get_password_hash
from app.core.config import FILE_PATH
from app.models.domain.Company import company
from app.models.domain.Department import department
from app.models.domain.Device import device
from app.models.domain.DeviceSetting import deviceSetting
from app.models.domain.DeviceUuid import deviceUuid
from app.models.domain.Error_handler import UnicornException
from app.models.domain.Face import face
# from app.models.domain.Face_Feature import face_feature
from app.models.domain.HardwareUuid import hardwareUuid
from app.models.domain.Observation import observation
from app.models.domain.Staff import staff
from app.models.domain.user import user


def change_user_level_to_hr(db: Session, user_id: int, level: int):
    user_db = db.query(user).filter(user.id == user_id).first()
    if level < 1 or level > 5:
        raise UnicornException(name=change_user_level_to_hr.__name__, description="權限 level 請輸入 1~5", status_code=400)
    db.begin()
    try:
        user_db.level = level
        user_db.updated_at = datetime.now()
        db.commit()
        db.refresh(user_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=change_user_level_to_hr.__name__, description=str(e), status_code=500)
    return user_db


def set_user_enable(db: Session, user_email: str):
    user_db = db.query(user).filter(user.email == user_email).first()
    if user_db.is_enable:
        raise HTTPException(status_code=202, detail="user 已啟用了")

    db.begin()
    try:
        user_db.is_enable = True
        user_db.updated_at = datetime.now()
        db.commit()
        db.refresh(user_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=set_user_enable.__name__, description=str(e), status_code=500)
    return user_db


def create_and_set_user_password(db: Session, user_email: str):
    user_db = db.query(user).filter(user.email == user_email).first()
    password = create_random_password()
    hashed_password = get_password_hash(password)

    db.begin()
    try:
        user_db.password = hashed_password
        user_db.updated_at = datetime.now()
        db.commit()
        db.refresh(user_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=create_and_set_user_password.__name__, description=str(e), status_code=500)
    return password


def clear_all_data(db: Session):
    db.begin()
    try:
        db.query(observation).delete()
        # db.query(face_feature).delete()
        db.query(face).delete()
        db.query(deviceSetting).delete()
        db.query(device).delete()
        db.query(hardwareUuid).delete()
        db.query(deviceUuid).delete()
        db.query(staff).delete()
        db.query(department).delete()
        db.query(company).delete()
        db.query(user).delete()

        if os.path.exists(FILE_PATH):
            if os.path.exists(FILE_PATH + "observation"):
                shutil.rmtree(FILE_PATH + "observation")

            if os.path.exists(FILE_PATH + "face"):
                shutil.rmtree(FILE_PATH + "face")

        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=clear_all_data.__name__, description=str(e), status_code=500)
    return "Done"
