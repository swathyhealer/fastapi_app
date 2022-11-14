from main import client

import pytest


class TestBookList:
    def test_book_list(self, admin_login_cred, create_user_initialization, user_login_initialization, book_data):

        json_body = create_user_initialization
        token_response = client.post("/login", data=admin_login_cred)
        access_token = token_response.json()["access_token"]
        response = client.post("/admin/user/create", json=json_body,
                               headers={"Authorization": f"Bearer {access_token}"})
        login_data = {
            "username": json_body["email"],
            "password": json_body["password"]
        }

        response = client.post("/login", data=login_data)
        access_token_user = response.json()["access_token"]

        response = client.get("/user/book/list", json=book_data,
                              headers={"Authorization": f"Bearer {access_token_user}"})
        assert response.status_code == 200
        assert response.json() != {}