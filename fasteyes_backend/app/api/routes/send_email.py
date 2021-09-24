from fastapi import APIRouter
from pydantic import EmailStr
from starlette.background import BackgroundTasks

from app.Server.send_email import send_email_async, send_email_background

router = APIRouter()


@router.get('/send-email/asynchronous')
async def send_email_asynchronous(title: str, email: str, name: str):
    await send_email_async(title, email,
                           {'title': title, 'name': name})
    return 'Success'


@router.get('/send-email/backgroundtasks')
def send_email_backgroundtasks(background_tasks: BackgroundTasks, title: str, email: str, name: str):
    send_email_background(background_tasks, title,
                          email, {'title': title, 'name': name})
    return 'Success'
