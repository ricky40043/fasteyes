from test_main import client

URL = "http://localhost:8000"


def test_add_user():
    url = URL + "/users"
    json = {
        "name": "ricky400430012345",
        "password": "ricky400430012345",
        "telephone_number": "0987654321",
        "email": "ricky400430012345@gmail.com",
        "address": "台北市中山區民權東路一段",
        "usage": "商用",
        "country": "Taiwan",
        "company_scale": "10~50",
        "industry": "軟體業",
        "level": 0
    }
    response = client.post(url, json=json)
    print("response:", response.json())
