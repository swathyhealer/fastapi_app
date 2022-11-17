import uuid


class TestUser:
    # python -m pytest => to run python pytest if module not found

    def test_create_user_fail_exists_email(self, create_user, admin_login):

        existing_username = create_user["email"]
        fake_user_data = {"email": existing_username, "password": "11er"}
        response = admin_login.post(
            "/admin/user/create",
            json=fake_user_data,
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "email already exists"

    def test_create_user_fail_no_username(self, admin_login):

        user_data = {"password": str(uuid.uuid4())}
        response = admin_login.post("/admin/user/create", json=user_data)

        assert response.status_code == 422

    def test_create_user_fail_no_username_no_password(self, admin_login):

        response = admin_login.post("/admin/user/create")

        assert response.status_code == 422
