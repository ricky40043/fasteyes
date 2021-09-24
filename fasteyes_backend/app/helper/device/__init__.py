from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.Server.device.crud import get_device_by_device_id, check_device_ower
from app.Server.authentication import checkLevel, Authority_Level
from app.models.domain.user import user


def check_Device_Authority(db: Session, current_user: user, device_id: int):
    if not checkLevel(current_user, Authority_Level.HRAccess.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    if get_device_by_device_id(db, device_id) is None:
        raise HTTPException(status_code=404, detail="device is not exist")

    device = check_device_ower(db, device_id, current_user.id)
    if device is None:
        if checkLevel(current_user, Authority_Level.Admin.value):
            device = get_device_by_device_id(device_id)
        else:
            raise HTTPException(status_code=401, detail="你不是裝置的使用者")

    return device
