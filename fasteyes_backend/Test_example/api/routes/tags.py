import json
import os
from random import randint

from Test.api.routes.products import test_create_products
from app.models.schemas.product import tagOut, productOut, productModify

from faker_schema.faker_schema import FakerSchema
from faker_schema.schema_loader import load_json_from_file, load_json_from_string
from Test.crud import clientFunc

tags_Create_schema = load_json_from_file(os.getcwd() + '\\Test\\tags_create.json')
faker = FakerSchema()
tags_Create_data_List = faker.generate_fake(tags_Create_schema, 10)

product_modify_f = open(os.getcwd() + '\\Test\\product_modify.json', )
product_modify = json.load(product_modify_f)

f = open(os.getcwd() + '\\Test\\register2.json', )
register_data2 = json.load(f)

f = open(os.getcwd() + '\\Test\\Login2.json', )
Login_data2 = json.load(f)

def test_delete_tags():
    clientFunc.delete("/tags/")


def test_tags_create():
    test_delete_tags()
    for tag in tags_Create_data_List:
        clientFunc.post("/tags/", 200, json=tag, validate_schema=tagOut.schema())


def test_tags_repeat_create():
    test_tags_create()
    tag1 = tags_Create_data_List[1]
    clientFunc.post("/tags/", 400, json=tag1, validate_data={'detail': "tag is exist"})


def test_tags_modify():
    test_tags_create()
    modify_tags = {"weight": randint(0, 15)}
    clientFunc.patch("/tags/1", 200, json=modify_tags, validate_schema=tags_Create_schema)


def test_tags_modify_not_exist():
    test_tags_create()
    modify_tags = {"weight": randint(0, 15)}
    clientFunc.patch("/tags/300", 400, json=modify_tags,
                     validate_data={"detail": "tag is not exist please create tag first"})


def test_tags_get():
    test_tags_create()
    clientFunc.get("/tags/5", 200, validate_schema=tagOut.schema())


def test_tags_get_not_exist():
    test_tags_create()
    clientFunc.get("/tags/200", 400, validate_schema={"detail": "tag is not exist"})


def test_tags_getAll():
    test_tags_create()
    clientFunc.get("/tags/", 200, validate_schema=tagOut.schema())


def test_product_patch_success():
    test_create_products()
    test_tags_create()
    clientFunc.patch("/products/1", 200, json=product_modify, validate_schema=productOut.schema(),
                     headers=clientFunc.get_current_user_header())

def test_product_patch_you_are_not_owner():
    test_create_products()
    test_tags_create()
    #創建第二個人並登入
    clientFunc.post("/users/register/",json=register_data2)
    clientFunc.Login(data=Login_data2)
    clientFunc.patch("/products/1", 400, json=product_modify, validate_data={"detail" : "You are not product owner"},
                     headers=clientFunc.get_current_user_header())


def test_product_patch_tags_not_exist():
    test_create_products()
    test_tags_create()
    num = 700
    product_modify["tags"] = [1, 5, 9, num]
    clientFunc.patch("/products/1", 400, json=product_modify, validate_data={"detail": f"tags {num} are not exist"},
                     headers=clientFunc.get_current_user_header())


def test_product_get_tag_1():
    test_create_products()
    test_tags_create()
    clientFunc.get("/products/1/tags", 200, validate_schema=tagOut.schema())


def test_product_get_tag_product_is_not_exist():
    test_create_products()
    test_tags_create()
    clientFunc.get("/products/100/tags", 400, validate_data={"detail": "product is not exist"})
