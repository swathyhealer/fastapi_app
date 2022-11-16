import pytest


class TestBookList:
    def test_book_list(self, user_login, get_client):

        access_token_user = user_login

        response = get_client.get(
            "/user/book/list", headers={"Authorization": f"Bearer {access_token_user}"}
        )
        assert response.status_code == 200
        assert response.json() != {}
