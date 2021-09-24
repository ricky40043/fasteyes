import os

from fastapi.testclient import TestClient

from app.main import app

URL = "http://localhost:8000"

json_data_path = os.getcwd() + "/test/json_data/"

client = TestClient(app)
