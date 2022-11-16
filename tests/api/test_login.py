import pytest


class TestLogin:
    def test_admin_login(self, admin_login):
        access_token = admin_login
        assert type(access_token) == str

    def test_user_login(self, user_login):
        access_token = user_login
        assert type(access_token) == str

    def test_login_unauthenticate(self, create_user, get_client):
        create_user_response = create_user[0]
        assert create_user_response.status_code == 200
        # NOTE: need shallow copy. otherwise data is getting change with each function
        user_data = create_user[1].copy()
        username = user_data.pop("email")
        user_data["username"] = username
        user_data["password"] = user_data["password"] + "_fail"

        response = get_client.post("/login", data=user_data)
        assert response.status_code == 401

    def test_login_email_validation_fail(self, create_user, get_client):

        create_user_response = create_user[0]
        assert create_user_response.status_code == 200
        # NOTE: need shallow copy. otherwise data is getting change with each function
        user_data = create_user[1].copy()
        username = user_data.pop("email")
        user_data["username"] = username + ".fail#"
        response = get_client.post("/login", data=user_data)
        assert response.status_code == 422
