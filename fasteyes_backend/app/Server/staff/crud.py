import io
import os
from datetime import datetime

from fastapi import File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from app.models.domain.Company import company
from app.models.domain.Error_handler import UnicornException
from app.models.domain.Face import face
from app.models.domain.Staff import staff
from app.models.domain.user import user
from app.models.schemas.Staff import StaffPatchViewModel
import cv2
import shutil
import uuid

from app.core.config import file_path


def get_staff_by_current_user(db: Session, current_user: user):
    Company_db = db.query(company).filter(company.user_id == current_user.id).first()
    return db.query(staff).filter(staff.company_id == Company_db.id).all()


def get_staff_by_company_id(db: Session, company_id: int):
    return db.query(staff).filter(staff.company_id == company_id).all()


def get_staff_by_SerialNumber(db: Session, SerialNumber: str, current_user: user):
    Company_db = db.query(company).filter(company.user_id == current_user.id).first()
    # return db.query(staff).filter(staff.company_id == Company_db.id).first()
    return db.query(staff).filter(staff.serial_number == SerialNumber, staff.company_id == Company_db.id).first()


def get_staff_by_SerialNumber_and_company(db: Session, SerialNumber: str, company_id: int):
    return db.query(staff).filter(staff.serial_number == SerialNumber, staff.company_id == company_id).first()


def get_staff_by_id(db: Session, staff_id: int):
    return db.query(staff).filter(staff.id == staff_id).first()


def check_staff_company(db: Session, staff_id: int, user_id: int):
    staff_db = db.query(staff).filter(staff.id == staff_id).first()
    conpany_db = db.query(company).filter(company.user_id == user_id).first()

    if staff_db is None:
        raise UnicornException(name=check_staff_company.__name__, description="staff is not exist", status_code=400)

    if conpany_db is None:
        raise UnicornException(name=check_staff_company.__name__, description="目前登入的使用者底下沒有公司", status_code=400)
    if staff_db.company_id == conpany_db.id:
        return True

    return False


def get_staff_email_exist(db: Session, email: str):
    return db.query(staff).filter(staff.email == email).first()


def get_staff_card_number_exists(db: Session, card_number: str):
    return db.query(staff).filter(staff.card_number == card_number).first()


def get_staff_face_images(db: Session, staff_id: int):
    return db.query(face).filter(face.staff_id == staff_id).all()


# 傳檔案
def get_staff_face_image_file(db: Session, staff_id: int, image_name: str):
    staff_db = db.query(staff).filter(staff.id == staff_id).first()
    Face_db = db.query(face).filter(face.staff_id == staff_id,
                                    face.face_uuid == image_name).first()
    if not Face_db:
        raise UnicornException(name=get_staff_face_image_file.__name__, description="face image not exist",
                               status_code=400)

    file_name = file_path + "face/company" + str(staff_db.company_id) + "/staff" + str(
        staff_db.id) + "/" + image_name + ".jpg"
    cv2img = cv2.imread(file_name)
    if cv2img is None:
        raise UnicornException(name=get_staff_face_image_file.__name__, description="face image not exist",
                               status_code=400)

    res, im_png = cv2.imencode(".jpg", cv2img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")


def upload_face_file(db: Session, staff_id: int, image: UploadFile = File(...)):
    db_staff = db.query(staff).filter(staff.id == staff_id).first()
    db_Company = db.query(company).filter(company.id == staff.company_id).first()

    db.begin()
    try:
        face_uuid = uuid.uuid4()
        while True:
            if db.query(face).filter(face.face_uuid == str(face_uuid)).first():
                face_uuid = uuid.uuid4()
            else:
                break
        upload_image(db_Company.id, db_staff.id, str(face_uuid), image)
        Face_db = face(staff_id=staff_id,
                       face_uuid=face_uuid)
        db.add(Face_db)
        db.commit()
        db.refresh(Face_db)

    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=modefy_Staff_Info.__name__, description=str(e), status_code=500)
    finally:
        image.file.close()
    return Face_db


def check_email_exist(db: Session, email: str):
    if db.query(staff).filter(staff.email == email).first():
        raise UnicornException(name=check_staff_company.__name__, description="email is exist", status_code=400)


def modefy_Staff_Info(db: Session, staff_id: int, staffPatch: StaffPatchViewModel):
    Staff_db = db.query(staff).filter(staff.id == staff_id).first()
    db.begin()
    try:
        if staffPatch.name:
            Staff_db.name = staffPatch.name
        if staffPatch.serial_number:
            Staff_db.serial_number = staffPatch.serial_number
        if staffPatch.card_number:
            Staff_db.card_number = staffPatch.card_number
        if staffPatch.telephone_number:
            Staff_db.telephone_number = staffPatch.telephone_number
        if staffPatch.cellphone_number:
            Staff_db.cellphone_number = staffPatch.cellphone_number
        if staffPatch.email:
            Staff_db.email = staffPatch.email
        if staffPatch.national_id_number:
            Staff_db.national_id_number = staffPatch.national_id_number
        if staffPatch.birthday:
            Staff_db.birthday = staffPatch.birthday
        if staffPatch.department_id:
            Staff_db.department_id = staffPatch.department_id
        if staffPatch.start_date:
            Staff_db.start_date = staffPatch.start_date
        if staffPatch.end_date:
            Staff_db.end_date = staffPatch.end_date

        Staff_db.status = staffPatch.status
        Staff_db.gender = staffPatch.gender

        Staff_db.updated_at = datetime.now()
        db.commit()
        db.refresh(Staff_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=modefy_Staff_Info.__name__, description=str(e), status_code=500)
    return Staff_db


def delete_Staff_by_Staff_id(db: Session, staff_id: int):
    Staff_db = db.query(staff).filter(staff.id == staff_id).first()
    db.begin()
    try:
        db.delete(Staff_db)
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=delete_Staff_by_Staff_id.__name__, description=str(e), status_code=500)
    return Staff_db


def delete_staff_all_image(db: Session, staff_id: int):
    Staff_db = db.query(staff).filter(staff.id == staff_id).first()
    db.begin()
    try:
        # 刪除全部照片和feature
        delete_all_image(Staff_db.company_id, staff_id)
        db.query(face).filter(face.staff_id == staff_id).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=delete_staff_all_image.__name__, description=str(e), status_code=500)
    return "Delete All Image Done"


def delete_feature(db: Session, staff_id: int):
    db.begin()
    try:
        staff_db = db.query(staff).filter(staff.id == staff_id).first()
        Company_id = db.query(company).filter(company.id == staff_db.company_id).first().id

        face_db = db.query(face).filter(face.staff_id == staff_id).first()
        face_db.updated_at = datetime.now()

        if os.path.exists(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id)):
            os.remove(file_path + "face/company" + str(Company_id) + "/staff" + str(
                staff_id) + "/" + "face_feature" + ".txt")

        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=delete_feature.__name__, description=str(e), status_code=500)
    return "Delete feature Done"


def delete_staff_image_by_image_name(db: Session, staff_id: int, image_name: str):
    staff_db = db.query(staff).filter(staff.id == staff_id).first()

    FaceFeature_db = db.query(face).filter(face.staff_id == staff_id,
                                           face.image_name == image_name).first()
    db.begin()
    try:
        delete_image(staff_db.company_id, staff_id, image_name)
        db.delete(FaceFeature_db)
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=delete_staff_image_by_image_name.__name__, description=str(e), status_code=500)
    return "Delete Image Done"


def check_staff_email_exsit(db: Session, email):
    if db.query(staff).filter(staff.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")


def upload_raw_face_feature(db: Session, staff_id, raw_face_feature: str):
    db.begin()
    try:
        staff_db = db.query(staff).filter(staff.id == staff_id).first()
        Company_id = db.query(company).filter(company.id == staff_db.company_id).first().id
        face_db = db.query(face).filter(face.staff_id == staff_id).first()
        face_db.updated_at = datetime.now()
        # 寫檔案
        if not os.path.exists(file_path + "face/"):
            os.mkdir(file_path + "face/")
        if not os.path.exists(file_path + "face/company" + str(Company_id)):
            os.mkdir(file_path + "face/company" + str(Company_id))
        if not os.path.exists(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id)):
            os.mkdir(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id))
        if not os.path.exists(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id)):
            os.mkdir(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id))

        path = file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id) + "/" + "face_feature" + ".txt"

        f = open(path, 'wb')

        f.write(raw_face_feature.encode())
        f.close()
        db.commit()

    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=delete_staff_image_by_image_name.__name__, description=str(e), status_code=500)
    return "Done"


def download_raw_face_feature(db: Session, staff_id):
    # 回傳檔案資料
    try:
        staff_db = db.query(staff).filter(staff.id == staff_id).first()
        Company_id = db.query(company).filter(company.id == staff_db.company_id).first().id
        # 寫檔案
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        if not os.path.exists(file_path + "face/"):
            os.mkdir(file_path + "face/")
        if not os.path.exists(file_path + "face/company" + str(Company_id)):
            os.mkdir(file_path + "face/company" + str(Company_id))
        if not os.path.exists(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id)):
            os.mkdir(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id))
        if not os.path.exists(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id)):
            os.mkdir(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id))

        path = file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id) + "/" + "face_feature" + ".jpg"
        f = open(path, 'wb')
        raw_face_feature = f.read()
        f.close()
        face_db = db.query(face).filter(face.staff_id == staff_id).first()

        raw_face_feature_data = {
            "id": face_db.id,
            "face_uuid": face_db.face_uuid,
            "updated_at": face_db.updated_at,
            "created_at": face_db.created_at,
            "staff_id": face_db.staff_id,
            "raw_face_feature": raw_face_feature
        }

    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=delete_staff_image_by_image_name.__name__, description=str(e), status_code=500)

    return raw_face_feature_data


def upload_image(Company_id: int, staff_id: int, image_name: str, image: UploadFile = File(...)):
    # 資料夾創建
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    if not os.path.exists(file_path + "face/"):
        os.mkdir(file_path + "face/")
    if not os.path.exists(file_path + "face/company" + str(Company_id)):
        os.mkdir(file_path + "face/company" + str(Company_id))
    if not os.path.exists(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id)):
        os.mkdir(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id))
    if not os.path.exists(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id)):
        os.mkdir(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id))

    with open(file_path + "face/company" + str(Company_id) + "/staff" + str(
            staff_id) + "/" + image_name + ".jpg", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)


def delete_image(Company_id: int, staff_id: int, image_name: str):
    if os.path.exists(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id)):
        os.remove(file_path + "face/company" + str(Company_id) + "/staff" + str(
            staff_id) + "/" + image_name + ".jpg")


def delete_all_image(Company_id: int, staff_id: int):
    if os.path.exists(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id)):
        shutil.rmtree(file_path + "face/company" + str(Company_id) + "/staff" + str(staff_id))
