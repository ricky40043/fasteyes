import base64
import io
import os
import shutil

import cv2
from fastapi import UploadFile
from sqlalchemy.orm import Session
from fastapi import File
from starlette.responses import StreamingResponse

from app.core.config import file_path
from app.models.domain.Error_handler import UnicornException
from app.models.domain.Observation import observation


def upload_observation_image(db: Session, device_id: int, image_name: str, image: UploadFile = File(...)):
    try:
        # 資料夾創建
        if not os.path.exists(file_path + "observation/"):
            os.mkdir(file_path + "observation/")
        if not os.path.exists(file_path + "observation/" + "device" + str(device_id)):
            os.mkdir(file_path + "observation/" + "device" + str(device_id))

        with open(file_path + "observation/" + "device" + str(device_id) + "/" + image_name + ".jpg", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        Observation_db = db.query(observation).filter(observation.image_name == image_name).first()
    except Exception as e:
        print(str(e))
        raise UnicornException(name=upload_observation_image.__name__, description=str(e), status_code=500)
    finally:
        image.file.close()

    return Observation_db


def download_observation_image(device_id: int, image_name: str):
    file_name = file_path + "observation/" + "device" + str(device_id) + "/" + image_name + ".jpg"
    cv2img = cv2.imread(file_name)
    res, im_png = cv2.imencode(".jpg", cv2img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")


def download_observation_image_base64(device_id: int, image_name: str):
    file_name = file_path + "observation/" + "device" + str(device_id) + "/" + image_name + ".jpg"
    cv2img = cv2.imread(file_name)
    while cv2img is None:
        cv2img = cv2.imread(file_name)

    res, im_png = cv2.imencode(".jpg", cv2img)
    jpg_as_text = base64.b64encode(im_png)
    return jpg_as_text


# def test_stream(device_id: int, image_name: str):
#     file_name = file_path+"observation/" + "device" + str(device_id) + "/" + image_name + ".jpg"
#     cv2img = cv2.imread(file_name)
#     res, im_png = cv2.imencode(".jpg", cv2img)
#     frame = im_png.tobytes()
#     while True:
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def delete_observation_image_by_id(db: Session, observation_id: int):
    observation_db = db.query(observation).filter(observation.id == observation_id).first()
    try:
        if os.path.exists(file_path + "observation/" + "device" + str(
                observation_db.device_id) + "/" + observation_db.image_name + ".jpg"):
            os.remove(file_path + "observation/" + "device" + str(
                observation_db.device_id) + "/" + observation_db.image_name + ".jpg")

    except Exception as e:
        print(str(e))
        raise UnicornException(name=delete_observation_image_by_id.__name__, description=str(e), status_code=500)
    return "Delete Image Done"


def delete_all_observation_image_by_device_id(device_id: int):
    try:
        if os.path.exists(file_path + "observation/" + "device" + str(device_id)):
            shutil.rmtree(file_path + "observation/" + "device" + str(device_id))

    except Exception as e:
        print(str(e))
        raise UnicornException(name=delete_observation_image_by_id.__name__, description=str(e), status_code=500)
    return "Delete Image Done"
