
import uuid
import pytest


@pytest.fixture
def create_user_initialization():
    random_email = str(uuid.uuid4())+"@gmail.com"

    user_data = {
        "email": random_email, "password": "password"
    }

    return user_data


@pytest.fixture
def user_login_initialization(create_user_initialization):
    user_id = create_user_initialization["email"]
    password = create_user_initialization["password"]
    login_data = {
        "username": user_id,
        "password": password

    }
    return login_data


@pytest.fixture
def admin_login_cred():

    admin_cred = {
        "username": "admin@gmail.com",
        "password": "hashed_password"

    }
    return admin_cred


@pytest.fixture
def book_data():

    return {
        "name": "book 1"
    }
