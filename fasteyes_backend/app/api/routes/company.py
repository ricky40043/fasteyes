from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.helper.authentication import Authorize_user
from app.helper.company import check_Company_Authority
from app.Server.company.crud import get_All_companies, create_company, \
    create_Staff_From_Company, delete_company_by_company_id, delete_All_staff_by_company_id, get_Company_by_company_id, \
    create_department_from_company, modify_department, get_department_by_id, delete_department_by_id, \
    Check_department_in_staffs, get_department_from_company, get_department_by_name, delete_departments_by_company_id, \
    get_department_staff_from_company
from app.Server.staff.crud import get_staff_by_company_id, check_staff_email_exsit, get_staff_by_SerialNumber, \
    get_staff_by_SerialNumber_and_company
from app.Server.authentication import checkLevel, Authority_Level
from app.db.database import get_db
from app.models.schemas.Company import CompanyViewModel, CompanyPostViewModel
from app.models.schemas.Department import DepartmentPostViewModel, DepartmentViewModel, DepartmentPatchViewModel, \
    Department_staffViewModel
from app.models.schemas.Staff import StaffViewModel, StaffPostViewModel

router = APIRouter()


# 公司ID 取得公司 (HRAccess)
@router.get("/Companies/{company_id}", response_model=CompanyViewModel)
def GetCompanyById(company_id: int, db: Session = Depends(get_db),
                   Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    return check_Company_Authority(db, current_user, company_id)


# 取得所有公司 (Admin)
@router.get("/Companies", response_model=List[CompanyViewModel])
def GetCompanies(db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    if not checkLevel(current_user, Authority_Level.Admin.value):
        raise HTTPException(status_code=401, detail="權限不夠")

    return get_All_companies(db)


# 公司ID 取得公司所有員工 (HRAccess)
@router.get("/Companies/{company_id}/staffs", response_model=List[StaffViewModel])
def GetStaffsByCompanyId(company_id: int, db: Session = Depends(get_db),
                         Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    company = check_Company_Authority(db, current_user, company_id)
    return get_staff_by_company_id(db, company.id)


# @router.post("/Companies", response_model=CompanyViewModel)
# def CreateCompany(companyIn: CompanyPostViewModel,
#                   db: Session = Depends(get_db),
#                   Authorize: AuthJWT = Depends()):
#     current_user = Authorize_user(Authorize, db)
#     if not checkLevel(current_user, Authority_Level.HRAccess.value):
#         raise HTTPException(status_code=401, detail="權限不夠")
#     return create_company(db, companyIn, current_user.id)

# 公司ID 創建員工 (HRAccess)
@router.post("/Companies/{company_id}/staffs", response_model=StaffViewModel)
def CreateStaffFromCompany(company_id: int, staffVM: StaffPostViewModel,
                           db: Session = Depends(get_db),
                           Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)

    check_Company_Authority(db, current_user, company_id)

    if get_staff_by_SerialNumber_and_company(db, staffVM.serial_number, company_id):
        raise HTTPException(status_code=400, detail="SerialNumber is exist")

    if not get_department_by_id(db, staffVM.department_id):
        raise HTTPException(status_code=400, detail="department id is not exist")

    return create_Staff_From_Company(db, company_id, staffVM)


# 公司ID 刪除公司 & 所有員工 & 所有部門 (HRAccess)
@router.delete("/Companies/{company_id}", response_model=CompanyViewModel)
def DeleteCompany(company_id: int,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Company_Authority(db, current_user, company_id)
    delete_All_staff_by_company_id(db, company_id)
    delete_departments_by_company_id(db, company_id)
    return delete_company_by_company_id(db, company_id)


# @router.delete("/Companies/{company_id}/staffs")
# def DeleteCompanyAllStaff(company_id: int,
#                           db: Session = Depends(get_db),
#                           Authorize: AuthJWT = Depends()):
#     current_user = Authorize_user(Authorize, db)
#     check_Company_Authority(db, current_user, company_id)
#     company = get_Company_by_company_id(db, company_id)
#     return delete_All_staff_by_company_id(db, company.id)


# 公司ID 取得所有部門 (HRAccess)
@router.get("/Companies/{company_id}/department", response_model=List[DepartmentViewModel])
def Get_department(company_id: int,
                   db: Session = Depends(get_db),
                   Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Company_Authority(db, current_user, company_id)
    return get_department_from_company(db, company_id)


# 公司ID 取得所有部門和部門底下所有員工 (HRAccess)
@router.get("/Companies/{company_id}/department_staff", response_model=List[Department_staffViewModel])
def Get_department_staff(company_id: int,
                         db: Session = Depends(get_db),
                         Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Company_Authority(db, current_user, company_id)
    return get_department_staff_from_company(db, company_id)


# 公司ID 新增部門 (HRAccess)
@router.post("/Companies/{company_id}/department", response_model=DepartmentViewModel)
def Create_department(company_id: int,
                      department: DepartmentPostViewModel,
                      db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Company_Authority(db, current_user, company_id)
    if get_department_by_name(db, department.name):
        raise HTTPException(status_code=400, detail="department name is exist")

    return create_department_from_company(db, company_id, department)


# 公司ID 修改部門 (HRAccess)
@router.patch("/Companies/{company_id}/department", response_model=DepartmentPatchViewModel)
def Modify_department(company_id: int,
                      department: DepartmentPatchViewModel,
                      db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Company_Authority(db, current_user, company_id)

    if not get_department_by_id(db, department.id):
        raise HTTPException(status_code=404, detail="department id is not exist")

    department_db = get_department_by_name(db, department.name)
    if department_db:
        if department_db.id != department.id:
            raise HTTPException(status_code=400, detail="department name is exist")

    return modify_department(db, department)


# 公司ID 刪除部門 (HRAccess)
@router.delete("/Companies/{company_id}/department/{department_id}", response_model=DepartmentViewModel)
def Delete_department(company_id: int,
                      department_id: int,
                      db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Company_Authority(db, current_user, company_id)

    if not get_department_by_id(db, department_id):
        raise HTTPException(status_code=404, detail="department is not exist")

    if Check_department_in_staffs(db, department_id):
        raise HTTPException(status_code=400, detail="department is use in staffs")

    return delete_department_by_id(db, department_id)


# 公司ID 刪除所有部門 (HRAccess)
@router.delete("/Companies/{company_id}/departments")
def Delete_department(company_id: int,
                      db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    current_user = Authorize_user(Authorize, db)
    check_Company_Authority(db, current_user, company_id)

    return delete_departments_by_company_id(db, company_id)


@router.get("/Companies/departments/{department_id}")
def Get_department_name(department_id: int,
                        db: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends()):
    Authorize_user(Authorize, db)
    if not get_department_by_id(db, department_id):
        raise HTTPException(status_code=404, detail="department id is not exist")

    return get_department_by_id(db, department_id)
