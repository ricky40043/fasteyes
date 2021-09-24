from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.Server.staff.crud import get_staff_by_id, check_staff_company, get_staff_by_SerialNumber
from app.Server.authentication import checkLevel, Authority_Level
from app.models.domain.user import user


#
def check_Staff_Authority(db: Session, current_user: user, staff_id: int):
    if not checkLevel(current_user, Authority_Level.HRAccess.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    staff = get_staff_by_id(db, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="staff is not exist")

    if not check_staff_company(db, staff_id, current_user.id):
        if checkLevel(current_user, Authority_Level.Admin.value):
            raise HTTPException(status_code=401, detail="staff不在登入的使用者的公司")
    return staff


def Check_Staff_Authority_SerialNumber(db: Session, current_user: user, SerialNumber: str):
    if not checkLevel(current_user, Authority_Level.HRAccess.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    staff = get_staff_by_SerialNumber(db, SerialNumber, current_user)
    if staff is None:
        raise HTTPException(status_code=404, detail="staff is not exist")

    return staff
