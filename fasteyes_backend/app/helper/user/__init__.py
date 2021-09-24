from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.Server.authentication import checkLevel, Authority_Level
from app.Server.user.crud import get_user_by_id
from app.models.domain.user import user


def ckeck_user_owner(db:Session, current_user:user, user_id: int):

    user_db = get_user_by_id(db, user_id)

    if not checkLevel(current_user, Authority_Level.HRAccess.value):
        raise HTTPException(status_code=401, detail="你還沒有權限")

    if user_db is None:
        raise HTTPException(status_code=404, detail="user is not exist")

    if user_id != current_user.id:
        if not checkLevel(current_user, Authority_Level.Admin.value):
            raise HTTPException(status_code=401, detail="你不是登入的使用者")

    return user_db
