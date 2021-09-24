import io
import json
import os
from pathlib import Path
from random import randint, choice

from faker_schema.faker_schema import FakerSchema
from faker_schema.schema_loader import load_json_from_file
from fastapi.testclient import TestClient

from app.main import app

URL = "http://localhost:8000"

json_file_path = os.getcwd() + "/test_add_user/"

client = TestClient(app)


def get_department_data():
    with open(json_file_path + 'department.json') as json_file:
        data = json.load(json_file)
    department_list = []
    for each_data in data:
        department_list.append(each_data["id"])
    return department_list


def get_json_data(name="header"):
    with open(json_file_path + name + '.json') as json_file:
        data = json.load(json_file)
    return data


def get_current_user_header(header_name="header"):
    with open(json_file_path + header_name + '.json') as json_file:
        data = json.load(json_file)
    return {"Authorization": "Bearer " + data["access_token"]}


def get_Default_Staff():
    url = URL + "/get-default-staff"
    response = client.get(url)
    data = response.json()
    return data["id"]


def test_clear_all_data():
    url = URL + "/auth/login"
    login_data = {
        "email": "ricky400430012@gmail.com",
        "password": "ricky400430012"
    }
    response = client.post(url, json=login_data)
    with open(json_file_path + 'header.json', 'w') as outfile:
        json.dump(response.json(), outfile)

    if response.status_code == 200:
        url = URL + "/auth/clear_all_data"
        response = client.delete(url, headers=get_current_user_header())
        print(response.json())
        assert response.status_code == 200


def test_add_Adminuser():
    url = URL + "/Adminusers"
    json_data = {
        "name": "ricky400430012",
        "password": "ricky400430012",
        "telephone_number": "0987654321",
        "email": "ricky400430012@gmail.com",
        "address": "台北市中山區民權東路一段",
        "usage": "商用",
        "country": "Taiwan",
        "company_scale": "10~50",
        "industry": "軟體業",
        "level": 0
    }
    response = client.post(url, json=json_data)
    print("response:", response.json())
    assert response.status_code == 200


def test_Login():
    url = URL + "/auth/login"
    login_data = {
        "email": "ricky400430012@gmail.com",
        "password": "ricky400430012"
    }
    response = client.post(url, json=login_data)
    with open(json_file_path + 'header.json', 'w') as outfile:
        json.dump(response.json(), outfile)
    assert response.status_code == 200


def test_create_company():
    test_Login()
    user_data = get_json_data()
    user_id = user_data["User"]["id"]
    url = URL + "/users/" + str(user_id) + "/companies"
    company = {
        "name": "123",
        "description": "ricky4004"
    }
    response = client.post(url, json=company, headers=get_current_user_header())
    print(response.json())
    assert response.status_code == 200


def test_create_5_department():
    test_Login()
    user_data = get_json_data()
    company_list = user_data["Company"]
    company_id = company_list[0]["id"]

    url = URL + "/Companies/" + str(company_id) + "/department"
    department_Create_schema = load_json_from_file(json_file_path + '/department_create.json')
    faker = FakerSchema()
    department_Create_data_List = faker.generate_fake(department_Create_schema, 5)

    for each_department_create_data in department_Create_data_List:
        each_department_create_data["description"] = ""
        response = client.post(url, json=each_department_create_data,
                               headers=get_current_user_header())
        print(response.json())
        assert response.status_code == 200


def test_get_department():
    test_Login()
    user_data = get_json_data()
    company_list = user_data["Company"]
    company_id = company_list[0]["id"]

    url = "/Companies/" + company_id + "/department"
    response = client.get(url, headers=get_current_user_header())
    with open(json_file_path + 'department.json', 'w') as outfile:
        json.dump(response.json(), outfile)


def test_create_default_staff():
    test_Login()
    user_data = get_json_data()
    company_list = user_data["Company"]
    company_id = company_list[0]["id"]

    url = URL + "/Companies/" + str(company_id) + "/staffs"
    staff_Create_schema = load_json_from_file(json_file_path + 'staff_create.json')
    faker = FakerSchema()
    staff_create_data = faker.generate_fake(staff_Create_schema, 1)

    department_list = get_department_data()
    staff_create_data["serial_number"] = "400430012"
    staff_create_data["name"] = "ricky"
    staff_create_data["gender"] = 0
    staff_create_data["department_id"] = choice(department_list)
    staff_create_data["status"] = 2
    response = client.post(url, json=staff_create_data,
                           headers=get_current_user_header())
    print(response.json())
    assert response.status_code == 200


def test_create_10_staff():
    test_Login()
    user_data = get_json_data()
    company_list = user_data["Company"]
    company_id = company_list[0]["id"]
    url = URL + "/Companies/" + str(company_id) + "/staffs"
    staff_Create_schema = load_json_from_file(json_file_path + 'staff_create.json')
    faker = FakerSchema()
    staff_Create_data_List = faker.generate_fake(staff_Create_schema, 10)
    department_list = get_department_data()
    for each_staff_create_data in staff_Create_data_List:
        each_staff_create_data["serial_number"] = randint(0, 1000)
        each_staff_create_data["gender"] = randint(0, 1)
        each_staff_create_data["department_id"] = choice(department_list)
        each_staff_create_data["status"] = randint(0, 2)
        response = client.post(url, json=each_staff_create_data,
                               headers=get_current_user_header())
        print(response.json())
        assert response.status_code == 200


def test_create_3_deviceUUID():
    url = URL + "/deviceUuids"
    for i in range(3):
        para = {"product_number": "Ricky" + str(i)}
        response = client.post(url, params=para, headers=get_current_user_header())
        print(response.json())
        assert response.status_code == 200

        with open(json_file_path + 'deviceuuid.json', 'w') as outfile:
            json.dump(response.json(), outfile)


def test_change_hardwareUUID():
    test_Login()
    device_data = get_json_data("deviceuuid")
    hardwareUuid_id = device_data["HardwareUUID"]["id"]
    url = URL + "/hardwareUuids/" + str(hardwareUuid_id)
    para = {"hardwareUuid": "b61fc353-54ba-463c-aab7-0687f705b419"}
    response = client.patch(url, params=para, headers=get_current_user_header())
    print(response.json())
    assert response.status_code == 200


def test_regist_device():
    user_data = get_json_data()
    user_id = user_data["User"]["id"]

    url = URL + "/hardwareUuids/search"
    json_data = {"hardwareuuid": "b61fc353-54ba-463c-aab7-0687f705b419"}
    response = client.post(url, json=json_data, headers=get_current_user_header())
    print(response.json())
    assert response.status_code == 200

    url = URL + "/devices"
    response_data = response.json()
    uuid = response_data["Hardware"]["device_uuid"]
    json_data = {
        "user_id": user_id,
        "name": "ricky4004",
        "description": "string",
        "device_uuid": uuid
    }
    response = client.post(url, json=json_data, headers=get_current_user_header())
    print(response.json())
    assert response.status_code == 200


def test_StaffFaceImages():
    staff_id = get_Default_Staff()
    url = URL + "/staffs/" + str(staff_id) + "/faces"
    path = json_file_path + 'default_staff/img.jpg'
    _files = {'Image_file': open(path, 'rb')}
    response = client.post(url, files=_files, headers=get_current_user_header())
    print(response.json())
    assert response.status_code == 200


def test_StaffFaceFeature():
    staff_id = get_Default_Staff()
    url = URL + "/staffs/" + str(staff_id) + "/raw_face_features"
    path = json_file_path + 'default_staff/face_feature.txt'
    f = open(path, 'rb')
    raw_face_feature = f.read()
    f.close()
    param = {"feature": raw_face_feature}
    response = client.post(url, params=param, headers=get_current_user_header())
    print(response.json())
    assert response.status_code == 200
