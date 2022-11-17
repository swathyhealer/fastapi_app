import uuid


class TestBook:
    def test_book_list(self, user_login):

        response = user_login.get(
            "/user/book/list",
        )
        assert response.status_code == 200
        assert response.json() != {}

    def test_update_book(self, user_login, add_book):

        book_id = add_book.json()["id"]
        # update
        response = user_login.put(
            "/user/book/" + str(book_id),
            params={"new_name": "modified new name"},
        )

        assert response.status_code == 200
        assert response.json() != {}
        assert "data" in response.json().keys()

    def test_update_book_fail_book_doesnt_exist(self, user_login):

        random_book_id = str(uuid.uuid4())
        response = user_login.put(
            "/user/book/" + str(random_book_id),
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "invalid book id"

    def test_update_book_fail_no_permission(self, add_book, alternate_user_login):

        added_book_id = add_book.json()["id"]

        response = alternate_user_login.put(
            "/user/book/" + str(added_book_id),
        )

        assert response.status_code == 401

    def test_delete_book(self, user_login, add_book):

        book_id = add_book.json()["id"]
        # delete
        response = user_login.delete(
            "/user/book/" + str(book_id),
        )
        assert response.status_code == 200
        assert response.json() != {}
        assert "data" in response.json().keys()

    def test_delete_book_fail_book_doesnt_exist(self, user_login):

        random_book_id = str(uuid.uuid4())
        response = user_login.delete(
            "/user/book/" + str(random_book_id),
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "invalid book id"

    def test_delete_book_fail_no_permission(
        self, user_login, alternate_user_login, get_book_name
    ):

        # add a new book
        response = user_login.post(
            "/user/book/add",
            json=get_book_name,
        )
        assert response.status_code == 200

        added_book_id = response.json()["id"]

        response = alternate_user_login.delete(
            "/user/book/" + str(added_book_id),
        )

        assert response.status_code == 401
