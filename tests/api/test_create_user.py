from main import client

import pytest


class TestUserCreate:
    # python -m pytest => to run python pytest if module not foundpe
    def test_create_normal_user(self, create_user_initialization, admin_login_cred):
        json_body = create_user_initialization
        token_response = client.post("/login", data=admin_login_cred)
        access_token = token_response.json()["access_token"]
        response = client.post("/admin/user/create", json=json_body,
                               headers={"Authorization": f"Bearer {access_token}"})
        self.username = json_body["email"]
        self.password = json_body["password"]

        assert response.status_code == 200
        assert response.json() != {}