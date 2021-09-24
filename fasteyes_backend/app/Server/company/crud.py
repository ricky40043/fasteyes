from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.domain.Company import company
from app.models.domain.Department import department
from app.models.domain.Error_handler import UnicornException
from app.models.domain.Staff import staff
from app.models.schemas.Company import CompanyViewModel
from app.models.schemas.Department import DepartmentPostViewModel
from app.models.schemas.Staff import StaffPostViewModel


def get_company_by_user_id(db: Session, user_id: int):
    return db.query(company).filter(company.user_id == user_id).all()


def get_Company_by_id(db: Session, company_id: int):
    return db.query(company).filter(company.id == company_id).first()


def check_company_ower(db: Session, company_id: int, user_id: int):
    return db.query(company).filter(company.id == company_id, company.user_id == user_id).first()


def check_Company_Exist(db: Session, company_id: int):
    db_company = db.query(company).filter(company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company is not exist")

    return db_company


def get_All_companies(db: Session):
    return db.query(company).all()


def get_Company_by_company_id(db: Session, company_id: int):
    return db.query(company).filter(company.id == company_id).first()


def create_company(db: Session, companyIn: CompanyViewModel, user_id):
    db.begin()
    try:
        db_Company = company(**companyIn.dict(),
                             user_id=user_id)
        db.add(db_Company)
        db.commit()
        db.refresh(db_Company)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=create_company.__name__, description=str(e), status_code=500)
    return db_Company


def create_Staff_From_Company(db: Session, company_id: int, StaffIn: StaffPostViewModel):
    db.begin()
    try:
        db_staff = staff(**StaffIn.dict(), company_id=company_id)
        db.add(db_staff)
        db.commit()
        db.refresh(db_staff)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=create_Staff_From_Company.__name__, description=str(e), status_code=500)
    return db_staff


def delete_company_by_company_id(db: Session, company_id: int):
    db_company = db.query(company).filter(company.id == company_id).first()
    db.begin()
    try:
        db.delete(db_company)
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=delete_company_by_company_id.__name__, description=str(e), status_code=500)
    return db_company


def delete_All_staff_by_company_id(db: Session, company_id: int):
    db.begin()
    try:
        db.query(staff).filter(staff.company_id == company_id).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=delete_All_staff_by_company_id.__name__, description=str(e), status_code=500)
    return "Delete staff Done"


def get_department_from_company(db: Session, company_id: int):
    return db.query(department).filter(department.company_id == company_id).all()


def get_department_staff_from_company(db: Session, company_id: int):
    department_db = db.query(department).filter(department.company_id == company_id).all()
    department_list = []
    for department_each in department_db:
        department_dict = department_each.to_dict()
        department_dict["member"] = []
        staff_list = db.query(staff).filter(staff.department_id == department_each.id).all()
        department_dict["member"] = staff_list
        department_list.append(department_dict)
    return department_list


def get_department_by_name(db: Session, name: str):
    return db.query(department).filter(department.name == name).first()


def create_department_from_company(db: Session, company_id: int, DepartmentIn: DepartmentPostViewModel):
    db.begin()
    try:
        db_department = department(**DepartmentIn.dict(), company_id=company_id)
        db.add(db_department)
        db.commit()
        db.refresh(db_department)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=create_department_from_company.__name__, description=str(e), status_code=500)
    return db_department


def get_department_by_id(db: Session, department_id: int):
    return db.query(department).filter(department.id == department_id).first()


def modify_department(db: Session, departmentIn: DepartmentPostViewModel):
    Department_db = db.query(department).filter(department.id == departmentIn.id).first()

    db.begin()
    try:
        Department_db.name = departmentIn.name
        Department_db.description = departmentIn.description
        db.commit()
        db.refresh(Department_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=modify_department.__name__, description=str(e), status_code=500)
    return Department_db


def delete_department_by_id(db: Session, department_id):
    Department_db = db.query(department).filter(department.id == department_id).first()
    db.begin()
    try:
        db.delete(Department_db)
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=delete_department_by_id.__name__, description=str(e), status_code=500)
    return Department_db


def delete_departments_by_company_id(db: Session, company_id):
    db.begin()
    try:
        db.query(department).filter(department.company_id == company_id).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=delete_department_by_id.__name__, description=str(e), status_code=500)
    return "Delete all departments Done"


def Check_department_in_staffs(db: Session, department_id):
    return db.query(staff).filter(staff.department_id == department_id).all()


def get_department_by_id(db: Session, department_id):
    return db.query(department).filter(department.id == department_id).first()
