import uuid

import pytest
from fastapi.testclient import TestClient

from helpers.common import CommonFunction
from main import app


@pytest.fixture(scope="module")
def get_client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="module")
def user_login(create_user, get_client):
    assert create_user[0].status_code == 200
    # NOTE: need shallow copy. otherwise data is getting change with each function
    user_data = create_user[1].copy()
    username = user_data.pop("email")
    user_data["username"] = username

    response = get_client.post("/login", data=user_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "access_token" in response_json.keys()
    return response_json["access_token"]


@pytest.fixture(scope="module")
def admin_login(get_client: TestClient):
    admin_json_path = "data.json"
    admin: dict = CommonFunction.read_json(admin_json_path)["admins"][0]
    _ = admin.pop("admin_id")
    username = admin.pop("email")
    admin["username"] = username

    response = get_client.post("/login", data=admin)
    assert response.status_code == 200
    response_json = response.json()
    assert "access_token" in response_json.keys()
    return response_json["access_token"]


@pytest.fixture(scope="module")
def get_book_name():
    book_name = str(uuid.uuid4) + "_book"
    return {"name": book_name}


@pytest.fixture(scope="module")
def create_user(admin_login, get_client):
    random_email = str(uuid.uuid4()) + "@gmail.com"
    random_password = str(uuid.uuid4())
    user_data = {"email": random_email, "password": random_password}

    response = get_client.post(
        "/admin/user/create",
        json=user_data,
        headers={"Authorization": f"Bearer {admin_login}"},
    )

    return response, user_data


@pytest.fixture(scope="module")
def add_book(user_login, get_client, get_book_name):

    user_access_token = user_login
    response = get_client.post(
        "/user/book/add",
        json=get_book_name,
        headers={"Authorization": f"Bearer {user_access_token}"},
    )
    assert response.status_code == 200
    assert response.json() != {}
    return response
