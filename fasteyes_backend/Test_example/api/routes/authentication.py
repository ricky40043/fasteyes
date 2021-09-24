import os


from Test.crud import clientFunc
from app.models.schemas.user import User, UserCreate, UserLogin_Response, UserOut

import json

from faker_schema.faker_schema import FakerSchema
from faker_schema.schema_loader import load_json_from_file, load_json_from_string

register_schema = load_json_from_file(os.getcwd() + '\\Test\\register.json')
faker = FakerSchema()
register_data_List = faker.generate_fake(register_schema, 10)

f = open(os.getcwd() + '\\Test\\register.json', )
register_data = json.load(f)

f = open(os.getcwd() + '\\Test\\response_Login.json', )
response_Login_data = json.load(f)

f = open(os.getcwd() + '\\Test\\register2.json', )
register_data2 = json.load(f)

f = open(os.getcwd() + '\\Test\\Login.json', )
Login_data = json.load(f)

def test_user_clear():
    clientFunc.post("/users/deleteAllUser", 200)


def test_register_fail():
    test_user_clear()
    clientFunc.post("/users/register/", 422)


def register_success():
    register_data["email"] = "ricky@gmail.com"
    clientFunc.post("/users/register/", 200, validate_schema=User.schema(), json=register_data)


def test_register_success():
    test_user_clear()
    register_success()

def test_register_Data_error():
    test_user_clear()
    register_data["email"] = "ricky"
    clientFunc.post("/users/register/", 422, validate_data={"detail": [
                                                                {
                                                                  "loc": [
                                                                    "body",
                                                                    "email"
                                                                  ],
                                                                  "msg": "value is not a valid email address",
                                                                  "type": "value_error.email"
                                                                }
                                                              ]
                                                            }, json=register_data)


def test_register_Email_exist():
    test_user_clear()
    register_success()
    clientFunc.post("/users/register/", 400, validate_data={"detail": "Email already registered"}, json=register_data)


def test_register_name_exist():
    test_user_clear()
    register_success()
    register_data["email"] = "ricky123@gmail.com"
    clientFunc.post("/users/register/", 400, validate_data={"detail": "name already exist"}, json=register_data)


def test_get_Users():
    test_user_clear()
    for each_register_data in register_data_List:
        clientFunc.post("/users/register/", 200, validate_schema=User.schema(), json=each_register_data)

    clientFunc.get("/users/get_users", 200, validate_schema=UserOut.schema())


def test_login_token():
    test_user_clear()
    register_success()
    clientFunc.Login("/token", 200, validate_schema=UserLogin_Response.schema(), data=Login_data)


def test_user_me_fail():
    test_user_clear()
    clientFunc.get("/user/me", 404, validate_data={"detail": "Not Found"}, headers=response_Login_data)


def test_user_me_success():
    test_user_clear()
    register_success()
    clientFunc.Login(data=Login_data)
    clientFunc.get("/users/me/", 200, validate_schema=User.schema(), headers=clientFunc.get_current_user_header())
