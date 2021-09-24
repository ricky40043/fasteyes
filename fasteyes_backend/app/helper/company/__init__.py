from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.Server.company.crud import check_company_ower, get_company_by_user_id, check_Company_Exist, get_Company_by_id
from app.Server.authentication import checkLevel, Authority_Level
from app.models.domain.user import user


def check_Company_Authority(db: Session, current_user: user, company_id: int):
    if not checkLevel(current_user, Authority_Level.HRAccess.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    check_Company_Exist(db, company_id)

    company = check_company_ower(db, company_id, current_user.id)

    if company is None:
        if checkLevel(current_user, Authority_Level.Admin.value):
            company = get_Company_by_id(db, company_id)
        else:
            raise HTTPException(status_code=401, detail="你不是公司的使用者")
    return company
