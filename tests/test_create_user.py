from main import client

import pytest


class TestFastApp:
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

    def test_login(self, admin_login_cred, create_user_initialization, user_login_initialization):
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
        response_json = response.json()
        assert response.status_code == 200
        assert response.json() != {}
        assert "access_token" in response.json().keys()

    def test_add_book(self, admin_login_cred, create_user_initialization, user_login_initialization, book_data):

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

        response = client.post("/user/book/add", json=book_data,
                               headers={"Authorization": f"Bearer {access_token_user}"})
        assert response.status_code == 200
        assert response.json() != {}
        assert ["name", "id", "status"] == list(response.json().keys())

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

    def test_delete_book(self, admin_login_cred, create_user_initialization, user_login_initialization, book_data):

        json_body = create_user_initialization
        # admin login
        token_response = client.post("/login", data=admin_login_cred)
        access_token = token_response.json()["access_token"]
        # create user
        response = client.post("/admin/user/create", json=json_body,
                               headers={"Authorization": f"Bearer {access_token}"})
        login_data = {
            "username": json_body["email"],
            "password": json_body["password"]
        }
        # userlogin
        response = client.post("/login", data=login_data)
        access_token_user = response.json()["access_token"]
        # add book
        add_response = client.post("/user/book/add", json=book_data,
                                   headers={"Authorization": f"Bearer {access_token_user}"})
        book_id = add_response.json()["id"]
        #delete
        response = client.delete(
            "/user/book/"+str(book_id), headers={"Authorization": f"Bearer {access_token_user}"})
        assert response.status_code == 200
        assert response.json() != {}
        assert "data" in response.json().keys()




    def test_update_book(self, admin_login_cred, create_user_initialization, user_login_initialization, book_data):

        json_body = create_user_initialization
        # admin login
        token_response = client.post("/login", data=admin_login_cred)
        access_token = token_response.json()["access_token"]
        # create user
        response = client.post("/admin/user/create", json=json_body,
                               headers={"Authorization": f"Bearer {access_token}"})
        login_data = {
            "username": json_body["email"],
            "password": json_body["password"]
        }
        # userlogin
        response = client.post("/login", data=login_data)
        access_token_user = response.json()["access_token"]
        # add book
        add_response = client.post("/user/book/add", json=book_data,
                                   headers={"Authorization": f"Bearer {access_token_user}"})
        book_id = add_response.json()["id"]
        #update
        response = client.put(
            "/user/book/"+str(book_id),params={"new_name":"modified new name"}, headers={"Authorization": f"Bearer {access_token_user}"})
        assert response.status_code == 200
        assert response.json() != {}
        assert "data" in response.json().keys()