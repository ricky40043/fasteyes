import json
from datetime import datetime

from jsonschema import validate
import os
from random import randint

from faker import Faker
from schema import Schema

from Test.api.routes.products import test_create_products
from app.models.schemas.borrow import borrowBook, borrowLend, borrowReturn
from app.models.schemas.product import tagOut, productOut, productModify
from main_test import client

from faker_schema.faker_schema import FakerSchema
from faker_schema.schema_loader import load_json_from_file, load_json_from_string
from Test.crud import clientFunc

tags_Create_schema = load_json_from_file(os.getcwd() + '\\Test\\tags_create.json')
faker = FakerSchema()
tags_Create_data_List = faker.generate_fake(tags_Create_schema, 10)

f = open(os.getcwd() + '\\Test\\Login.json', )
Login_data = json.load(f)

f = open(os.getcwd() + '\\Test\\Login2.json', )
Login_data2 = json.load(f)

f = open(os.getcwd() + '\\Test\\register2.json', )
register_data2 = json.load(f)

f = open(os.getcwd() + '\\Test\\Login2.json', )
Login_data2 = json.load(f)


def test_delete_all_record():
    client.delete("/borrows/delete_all_record")


def test_booking_fail_borrow_to_owner():
    test_delete_all_record()
    test_create_products()
    time_now = {"book_time": datetime.now()}
    clientFunc.post("/borrows/booking/2", 400, validate_data={"detail": "Product can't borrow to owner"},
                    headers=clientFunc.get_current_user_header(), params=time_now)


def test_booking_product_not_exist():
    test_delete_all_record()
    test_create_products()
    time_now = {"book_time": datetime.now()}
    # 登入第二個人
    clientFunc.post("/users/register/", json=register_data2)
    clientFunc.Login(data=Login_data2)
    clientFunc.post("/borrows/booking/100", 400, validate_data={"detail": "product is not exist"},
                    headers=clientFunc.get_current_user_header(), params=time_now)


def test_booking_success():
    test_delete_all_record()
    test_create_products()
    time_now = {"book_time": datetime.now()}
    # 登入第二個人
    clientFunc.post("/users/register/", json=register_data2)
    clientFunc.Login(data=Login_data2)
    clientFunc.post("/borrows/booking/2", 200, validate_schema=borrowBook.schema(),
                    headers=clientFunc.get_current_user_header(), params=time_now)


def test_booking_is_booked():
    test_booking_success()
    time_now = {"book_time": datetime.now()}
    clientFunc.post("/borrows/booking/1", 400, validate_data={"detail": "is booked"},
                    headers=clientFunc.get_current_user_header(), params=time_now)


def test_borrows_lend_form_to_list_not_exist():
    test_booking_success()
    time_now = {"book_time": datetime.now()}
    clientFunc.post("/borrows/lend/10", 400, validate_data={"detail": "form_to list does not exist"},
                    headers=clientFunc.get_current_user_header(), params=time_now)


def test_borrows_lend_you_are_not_owner():
    test_booking_success()
    time_now = {"book_time": datetime.now()}
    clientFunc.post("/borrows/lend/10", 400, validate_data={"detail": "form_to list does not exist"},
                    headers=clientFunc.get_current_user_header(), params=time_now)


def test_borrows_lend_success():
    test_booking_success()
    # 登入第一個人
    clientFunc.Login(data=Login_data)
    time_now = {"book_time": datetime.now()}
    clientFunc.post("/borrows/lend/1", 200, validate_schema=borrowLend.schema(),
                    headers=clientFunc.get_current_user_header(), params=time_now)


def test_borrows_return_back_form_to_list_not_exist():
    test_borrows_lend_success()
    time_now = {"book_time": datetime.now()}
    clientFunc.post("/borrows/returns/10", 400, validate_data={"detail": "form_to list does not exist"},
                    headers=clientFunc.get_current_user_header(), params=time_now)


def test_borrows_return_back_you_are_not_borrow_person():
    test_borrows_lend_success()
    time_now = {"book_time": datetime.now()}
    clientFunc.post("/borrows/returns/1", 400, validate_data={"detail": "you are not the borrow person"},
                    headers=clientFunc.get_current_user_header(), params=time_now)


def test_borrows_return_success():
    test_borrows_lend_success()
    clientFunc.Login(data=Login_data2)
    time_now = {"book_time": datetime.now()}
    clientFunc.post("/borrows/returns/1", 200, validate_schema = borrowReturn.schema(),
                    headers=clientFunc.get_current_user_header(), params=time_now)


def test_borrows_return_is_return_back():
    test_borrows_return_success()
    time_now = {"book_time": datetime.now()}
    clientFunc.post("/borrows/returns/1", 400, validate_data = {"detail": "is return back"},
                    headers=clientFunc.get_current_user_header(), params=time_now)