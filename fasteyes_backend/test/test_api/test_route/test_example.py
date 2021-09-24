# import io
import json
import os

from test import client, URL, json_data_path

f = open(json_data_path + 'login_data.json', )
login_data = json.load(f)

f = open(json_data_path + 'adminuser_data.json', encoding='utf8')
adminusers_data = json.load(f)


def get_json_data(name="header"):
    with open(json_data_path + name + '.json') as json_file:
        data = json.load(json_file)
    return data


def get_current_user_header(header_name="header"):
    with open(json_data_path + header_name + '.json') as json_file:
        data = json.load(json_file)
    return {"Authorization": "Bearer " + data["access_token"]}


def test_clear_all_data():
    url = URL + "/auth/login"
    response = client.post(url, json=login_data)
    with open(json_data_path + 'header.json', 'w') as outfile:
        json.dump(response.json(), outfile)

    if response.status_code == 200:
        url = URL + "/auth/clear_all_data"
        response = client.delete(url, headers=get_current_user_header())
        print(response.json())
        assert response.status_code == 200


def test_add_Adminuser():
    url = URL + "/Adminusers"
    response = client.post(url, json=adminusers_data)
    print("response:", response.json())
    # assert response.status_code == 200


def test_Login():
    url = URL + "/auth/login"
    response = client.post(url, json=login_data)
    with open(json_data_path + 'header.json', 'w') as outfile:
        json.dump(response.json(), outfile)
    print("response:", response.json())
    assert response.status_code == 200
