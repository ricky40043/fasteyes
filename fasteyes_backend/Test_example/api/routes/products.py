import json
from random import randint

import os

from schema import Schema, And, Use
from faker import Faker

from Test.crud import clientFunc
from app.models.schemas.product import productOut
from main_test import client

from faker_schema.faker_schema import FakerSchema
from faker_schema.schema_loader import load_json_from_file, load_json_from_string
from Test.api.routes.authentication import register_success, test_user_clear

product_Create_schema = load_json_from_file(os.getcwd() + '\\Test\\product_create.json')
faker = FakerSchema()
product_Create_data_List = faker.generate_fake(product_Create_schema, 10)

f = open(os.getcwd() + '\\Test\\response_product_create.json', )
response_product_create_data = json.load(f)

f = open(os.getcwd() + '\\Test\\Login.json', )
Login_data = json.load(f)

f = open(os.getcwd() + '\\Test\\register2.json', )
register_data2 = json.load(f)

f = open(os.getcwd() + '\\Test\\Login2.json', )
Login_data2 = json.load(f)

schema = Schema({'name': str,
                 'id': And(Use(int), lambda n: n >= 0),
                 'borrow_time_limit': And(Use(int), lambda n: 1 <= n <= 15),
                 'is_rented': bool,
                 'borrow_count': And(Use(int), lambda n: n >= 0),
                 'user_id': And(Use(int), lambda n: n >= 0),
                 'category': str,
                 })
schema_list = Schema([schema])


def test_products_clear():
    response = client.post("/products/deleteAllproduct")
    assert response.status_code == 200


def test_create_products():
    test_products_clear()
    test_user_clear()
    register_success()
    clientFunc.Login(data=Login_data)
    for each_product_create_data in product_Create_data_List:
        each_product_create_data["borrow_time_limit"] = randint(1, 15)
        clientFunc.post("/products/", json=each_product_create_data,
                        validate_schema=response_product_create_data,
                        headers=clientFunc.get_current_user_header())


def test_get_my_products():
    test_create_products()
    clientFunc.get("/users/me/products", 200, validate_schema=productOut.schema(),
                   headers=clientFunc.get_current_user_header())


def test_get_user_1_products():
    test_create_products()
    clientFunc.get("users/1/product", 200, validate_schema=productOut.schema())


def test_get_user_5_products():
    test_create_products()
    clientFunc.get("users/5/product", 200, validate_schema=productOut.schema())


def test_get_products():
    test_create_products()
    clientFunc.get("/products/", 200, validate_schema=productOut.schema())


def test_get_product_1():
    test_create_products()
    clientFunc.get("/products/1", 200, validate_schema = productOut.schema())


def test_Delete_products_success():
    test_create_products()
    clientFunc.delete("/products/5", validate_data={"message" :"Delete Done"}, headers=clientFunc.get_current_user_header())


def test_Delete_products_is_not_exist():
    test_create_products()
    clientFunc.delete("/products/5", headers=clientFunc.get_current_user_header())
    clientFunc.delete("/products/5",400, validate_data={"detail" : "product is not exist"}, headers=clientFunc.get_current_user_header())


def test_Delete_products_worng_owner():
    test_create_products()
    #創建第二個人並登入
    clientFunc.post("/users/register/",json=register_data2)
    clientFunc.Login(data=Login_data2)
    clientFunc.delete("/products/5",400, validate_data={"detail" : "You are not this product owner"}, headers=clientFunc.get_current_user_header())


def test_Search_products():
    fake = Faker()
    for i in range(100):
        name = fake.name()
        clientFunc.get("/products/search/" + name, 200, validate_schema=productOut.schema())
