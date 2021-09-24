import json as jsonFunc

from schema import Schema

from main_test import client
from jsonschema import validate
import os


def Login(url="/token", validate_status_code=200, header_name="header", validate_data=None, validate_schema=None,
          data=None,json=None, **kwargs):
    response = post(url, validate_status_code, validate_data, validate_schema, data, json, **kwargs)
    with open(os.getcwd() + '\\' + header_name + '.json', 'w') as outfile:
        jsonFunc.dump(response.json(), outfile)


def get_current_user_header(header_name="header"):
    with open(os.getcwd() + '\\' + header_name + '.json') as json_file:
        data = jsonFunc.load(json_file)
    # print(data)
    return {"Authorization": "Bearer " + data["access_token"]}


def post(url, validate_status_code=200, validate_data=None, validate_schema=None, data=None, json=None, **kwargs):
    response = client.post(url, data=data, json=json, **kwargs)
    print("response:", response.json())
    print("response status_code:", response.status_code)

    if validate_data:
        assert response.json() == validate_data

    if validate_schema:
        if isinstance(response.json(), list):
            for each_response in response.json():
                assert validate(instance=each_response, schema=validate_schema) is None
        else:
            assert validate(instance=response.json(), schema=validate_schema) is None

    return response


def get(url, validate_status_code=200, validate_data=None, validate_schema=None, **kwargs):
    response = client.get(url, **kwargs)
    print("response:", response.json())
    print("response status_code:", response.status_code)
    assert response.status_code == validate_status_code

    if validate_data:
        assert response.json() == validate_data

    if validate_schema:
        if isinstance(response.json(), list):
            for each_response in response.json():
                assert validate(instance=each_response, schema=validate_schema) is None
        else:
            assert validate(instance=response.json(), schema=validate_schema) is None

    return response


def patch(url, validate_status_code=200, validate_data=None, validate_schema=None, data=None, **kwargs):
    response = client.patch(url, data=data, **kwargs)
    print("response:", response.json())
    print("response status_code:", response.status_code)
    assert response.status_code == validate_status_code

    if validate_data:
        assert response.json() == validate_data

    if validate_schema:
        if isinstance(response.json(), list):
            for each_response in response.json():
                assert validate(instance=each_response, schema=validate_schema) is None
        else:
            assert validate(instance=response.json(), schema=validate_schema) is None

    return response


def delete(url, validate_status_code=200, validate_data=None, validate_schema=None, **kwargs):
    response = client.delete(url, **kwargs)
    print("response:", response.json())
    print("response status_code:", response.status_code)
    assert response.status_code == validate_status_code

    if validate_data:
        assert response.json() == validate_data

    if validate_schema:
        if isinstance(response.json(), list):
            for each_response in response.json():
                assert validate(instance=each_response, schema=validate_schema) is None
        else:
            assert validate(instance=response.json(), schema=validate_schema) is None

    return response
