

import pytest
import uuid

class TestUpdateBook:


   def test_update_book(self,user_login, add_book,get_client):

        
        access_token_user=user_login
        book_id = add_book.json()["id"]
        #update
        response = get_client.put(
            "/user/book/"+str(book_id),params={"new_name":"modified new name"}, headers={"Authorization": f"Bearer {access_token_user}"})
        assert response.status_code == 200
        assert response.json() != {}
        assert "data" in response.json().keys()


   def test_update_book_fail_book_doesnt_exist(self,user_login,get_client):
        access_token_user=user_login
        random_book_id=str(uuid.uuid4())
        response = get_client.put(
            "/user/book/"+str(random_book_id), headers={"Authorization": f"Bearer {access_token_user}"})
        assert response.status_code == 400
        assert response.json()["detail"]=="invalid book id"

   def test_update_book_fail_no_permission(self,admin_login,user_login,get_client,get_book_name):
        
        #add a new book
        user_access_token=user_login
        response = get_client.post("/user/book/add", json=get_book_name,
                               headers={"Authorization": f"Bearer {user_access_token}"})
        assert response.status_code == 200

        added_book_id=response.json()["id"]

      
        # create user who is not  owner of the book
        random_email = str(uuid.uuid4())+"@gmail.com"
        random_password=str(uuid.uuid4())
        fake_owner_data = {
            "email": random_email, "password": random_password
        }
    
        fake_user_response = get_client.post("/admin/user/create", json=fake_owner_data,
                                headers={"Authorization": f"Bearer {admin_login}"})
        assert fake_user_response.status_code==200
        # create access token for fake owner
        username=fake_owner_data.pop("email")
        fake_owner_data["username"]=username
        response = get_client.post("/login", data=fake_owner_data)
        
        fake_owner_access_token= response.json()["access_token"]
        response = get_client.put(
            "/user/book/"+str(added_book_id), headers={"Authorization": f"Bearer {fake_owner_access_token}"})
        
        assert response.status_code == 401
       