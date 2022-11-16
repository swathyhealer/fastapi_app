import pytest


class TestUserCreate:
    # python -m pytest => to run python pytest if module not foundpe
    def test_create_normal_user(self, create_user):
        response = create_user[0]

        assert response.status_code == 200
        assert ["email", "user_id", "created_by"] == list(response.json().keys())

    def test_create_user_fail_exists_email(self, create_user, admin_login, get_client):
        response = create_user[0]

        assert response.status_code == 200
        existing_username = response.json()["email"]
        fake_user_data = {"email": existing_username, "password": "11er"}
        response = get_client.post(
            "/admin/user/create",
            json=fake_user_data,
            headers={"Authorization": f"Bearer {admin_login}"},
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "email already exists"
