def test_user_registation(client):
    data = {
        "name": "Subham",
        "email": "subham@gmail.com",
        "password": "test123",
        "city_id": 1
    }

    response = client.post("/user/register", json=data)
    assert response.status_code == 201

    response_data = response.json()

    assert response_data['name'] == "Subham"
    assert response_data['email'] == "subham@gmail.com"
    assert response_data['city_id'] == 1

def test_resgistaion_with_duplicate_email(client):
    data = {
        "name": "Subham",
        "email": "subham@gmail.com",
        "password": "test123",
        "city_id": 1
    }
    response = client.post("/user/register", json=data)
    duplicate_data = {
        "name": "Anubhab",
        "email": "subham@gmail.com",
        "password": "test098",
        "city_id": 2
    }
    response = client.post("/user/register", json=duplicate_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_users(client):

    data = {
        "name": "Subham",
        "email": "subham@gmail.com",
        "password": "test123",
        "city_id": 1
    }
    client.post("/user/register", json=data)
    
    payload = {
        "username": "subham@gmail.com",
        "password": "test123"
    }

    response = client.post("/user/login", data=payload)
    login_response = response.json()
    assert response.status_code == 200
    assert "access_token" in login_response
    assert login_response['token_type'] == "bearer"
    
def test_login_user_wrong_password(client):

    data = {
        "name": "Subham",
        "email": "subham@gmail.com",
        "password": "test123",
        "city_id": 1
    }
    client.post("/user/register", json=data)
    
    payload = {
        "username": "subham@gmail.com",
        "password": "Tesa098"
    }
    response = client.post("/user/login", data=payload)

    assert response.status_code == 401
    


def test_get_my_profile(client, user_headers):
    response = client.get("/user/me", headers=user_headers)
    assert response.status_code == 200

    user_data = response.json()
    assert user_data['name'] == "Subham"
    assert user_data['email'] == "subham@gmail.com"
    assert user_data['city_id'] == 1
    assert "password" not in user_data

def test_get_my_profile_without_token(client):

    response = client.get("/user/me")
    assert response.status_code == 401

def test_get_my_profile_invalid_token(client):

    response = client.get("/user/me", headers={"Authorization": "Bearer fyeshdgdb"})
    assert response.status_code == 401
    

def test_change_my_password(client, user_headers):

    password = {
       "current_password": "test123",
       "new_password": "subham123"
    }
    response = client.put("/user/me/password", json= password, headers=user_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

def test_change_my_password_wrong_password(client, user_headers):
    password = {
       "current_password": "sssssss",
       "new_password": "subham123"
    }
    response = client.put("/user/me/password", json= password, headers=user_headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Current password is incorrect"
   