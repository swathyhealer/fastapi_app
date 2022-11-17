import uuid

import pytest
from fastapi.testclient import TestClient

from helpers.common import CommonFunction
from main import app


# @pytest.fixture(scope="module")
def get_client():
    client = TestClient(app)
    return client


def user_helper_login(cred: dict):
    client = get_client()

    response = client.post("/login", data=cred)
    assert response.status_code == 200
    response_json = response.json()
    assert "access_token" in response_json.keys()
    client.headers.update({"Authorization": f"Bearer {response_json['access_token']}"})
    return client


@pytest.fixture(scope="module")
def naive_session():
    return get_client()


@pytest.fixture(scope="module")
def admin_login():
    admin_json_path = "data.json"
    admin: dict = CommonFunction.read_json(admin_json_path)["admins"][0]
    _ = admin.pop("admin_id")
    username = admin.pop("email")
    admin["username"] = username

    return user_helper_login(admin)


@pytest.fixture(scope="module")
def user_login(create_user):

    # NOTE: need shallow copy. otherwise data is getting change with each function
    user_data = create_user.copy()
    username = user_data.pop("email")
    user_data["username"] = username

    # return client
    return user_helper_login(user_data)


@pytest.fixture(scope="module")
def get_book_name():
    book_name = str(uuid.uuid4) + "_book"
    return {"name": book_name}


@pytest.fixture(scope="module")
def create_user(admin_login):
    random_email = str(uuid.uuid4()) + "@gmail.com"
    random_password = str(uuid.uuid4())
    user_data = {"email": random_email, "password": random_password}

    response = admin_login.post(
        "/admin/user/create",
        json=user_data,
    )
    # print(admin_login.__dict__)
    assert response.status_code == 200
    return user_data


@pytest.fixture(scope="module")
def create_alternate_user(admin_login):
    random_email = str(uuid.uuid4()) + "@gmail.com"
    random_password = str(uuid.uuid4())
    user_data = {"email": random_email, "password": random_password}

    response = admin_login.post(
        "/admin/user/create",
        json=user_data,
    )
    print(admin_login.__dict__)
    assert response.status_code == 200
    return user_data


@pytest.fixture(scope="module")
def alternate_user_login(create_alternate_user):
    # get_client:TestClient=create_alternate_user[0]
    # NOTE: need shallow copy. otherwise data is getting change with each function
    user_data = create_alternate_user.copy()
    username = user_data.pop("email")
    user_data["username"] = username

    return user_helper_login(user_data)


@pytest.fixture(scope="module")
def add_book(user_login, get_book_name):

    response = user_login.post("/user/book/add", json=get_book_name)
    assert response.status_code == 200
    assert response.json() != {}
    return response
