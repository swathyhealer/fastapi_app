class TestLogin:
    def test_login_unauthenticate(self, create_user, naive_session):

        # NOTE: need shallow copy. otherwise data is getting change with each function
        user_data = create_user.copy()
        username = user_data.pop("email")
        user_data["username"] = username
        user_data["password"] = user_data["password"] + "_fail"

        response = naive_session.post("/login", data=user_data)
        assert response.status_code == 401

    def test_login_email_validation_fail(self, create_user, naive_session):

        # NOTE: need shallow copy. otherwise data is getting change with each function
        user_data = create_user.copy()
        username = user_data.pop("email")
        user_data["username"] = username + ".fail#"
        response = naive_session.post("/login", data=user_data)
        assert response.status_code == 422
