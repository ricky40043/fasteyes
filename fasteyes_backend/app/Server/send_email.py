import os
from typing import List

import jwt
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.Server.authentication import SECRET_KEY, create_access_token
from app.Server.observation_file.crud import download_observation_image_base64
from app.Server.staff.crud import get_staff_by_id
from app.core.config import HOST_NAME
from dotenv import load_dotenv
load_dotenv('.env')


class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')


conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER='./templates'
)


async def send_email_async(subject: str, email_to: str, body: dict):
    print(subject)
    print(email_to)
    print(body)
    verify_code = body["verify_code"]

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        subtype='html',
        body=body
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')


def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict):
    template = f"""
           <html>
               <body">
                     <h1>
                        員工編號: {body["serial_number"]}
                     </h1>
                     <h2>
                        員工姓名: {body["name"]}
                     </h2>
                     <h2>
                        員工溫度:{body["observation"]["temperature"]}
                     </h2>
                     <h2>
                        員工觀測結果:{body["observation"]["id"]}        
                     </h2>
                    <a href="{HOST_NAME}/Files/download/image/device/{body["observation"]["device_id"]}/file_name/{body["observation"]["image_name"]}" />
            </body>
           </html>        
       """
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=template,
        subtype='html',
    )

    fm = FastMail(conf)

    background_tasks.add_task(
        fm.send_message, message)


async def send_Verfiy_code_email_async(email: str, verify_code: str):
    title = "fasteyes verify Code"
    template = f"""
           <html>
               <body">
                     <h1>
                     {verify_code}
                     </h1>
               </body>
           </html>        
       """
    message = MessageSchema(
        subject=title,
        recipients=[email],
        subtype='html',
        body=template
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')


async def SendEmailVerficationEmail(email: str):
    token_data = {
        "username": email
    }

    token = create_access_token(token_data)

    template = f"""
        <html>
            <body">
                  <a href="{HOST_NAME}/auth/verify_email?token={token}">
                  </a>
            </body>
        </html>        
    """
    message = MessageSchema(
        subject="Email verification",
        recipients=[email],
        subtype='html',
        body=template
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')


async def SendForgetPasswordEmail(email: str, password):
    template = password

    message = MessageSchema(
        subject="forget password",
        recipients=[email],
        body=template
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')


def send_email_temperature_alert(background_tasks: BackgroundTasks, db: Session, email: str, observation_db):
    title = "溫度異常"
    staff_db = get_staff_by_id(db, observation_db.staff_id)
    if staff_db:
        name = staff_db.name
        serial_number = staff_db.serial_number
    else:
        name = "Unknow"
        serial_number = "None"

    send_email_background(background_tasks, title, email,
                          {'title': title, 'name': name, 'observation': observation_db.to_dict(),
                           'serial_number': serial_number})
