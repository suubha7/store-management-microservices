def test_get_users(client, admin_headers):

    response = client.get("/admin/users", headers=admin_headers)
    assert response.status_code == 200
    users = response.json()

    assert isinstance(users, list)
    assert len(users) > 0

def test_get_users_with_users_token(client, user_headers):

    response = client.get("/admin/users", headers=user_headers)
    assert response.status_code == 403

def test_get_users_without_token(client):

    response = client.get("/admin/users")
    assert response.status_code == 401

def test_get_user_by_id(client, admin_headers):

    response = client.get("/admin/user/1", headers=admin_headers)
    assert response.status_code == 200

    user = response.json()
    assert user['email'] == "admin@gmail.com"

def test_get_user_by_wrong_id(client, admin_headers):

    response = client.get("/admin/user/2", headers=admin_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_update_user_status_by_id(client, admin_headers):

    response = client.put("/admin/user/update_status/1", json={"is_active": False},headers=admin_headers)
    assert response.status_code == 200

    assert response.json()['is_active'] == False

def test_update_user_status_by_wrong_id(client, admin_headers):

    response = client.put("/admin/user/update_status/2", json={"is_active": False}, headers=admin_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_delete_user_by_id(client, admin_headers):

    response = client.delete("/admin/user/delete/1", headers= admin_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"

def test_delete_user_by_wrong_id(client, admin_headers):

    response = client.delete("/admin/user/delete/2", headers= admin_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"