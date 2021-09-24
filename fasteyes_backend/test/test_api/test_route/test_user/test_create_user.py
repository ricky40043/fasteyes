# import io
import json
import os

from test import client, URL, json_data_path

from test.test_api.test_route.test_example import test_Login, get_current_user_header

f = open(json_data_path + 'user_data.json', encoding='utf8')
users_data = json.load(f)


def test_add_user_successful():
    test_Login()
    url = URL + "/users"
    response = client.post(url, json=users_data, headers=get_current_user_header())
    print("response:", response.json())
    assert response.status_code == 200


def test_add_user_email_exist():
    test_Login()
    url = URL + "/users"
    validate_data = {"detail": "Email already registered"}
    response = client.post(url, json=users_data, headers=get_current_user_header())
    print("response:", response.json())
    assert response.status_code == 400
    assert response.json() == validate_data


def test_add_user_name_exist():
    test_Login()
    url = URL + "/users"
    users_data["email"] = "rrrrrr@gmail.com"
    validate_data = {"detail": "Name already exist"}
    response = client.post(url, json=users_data, headers=get_current_user_header())
    print("response:", response.json())
    assert response.status_code == 400
    assert response.json() == validate_data
