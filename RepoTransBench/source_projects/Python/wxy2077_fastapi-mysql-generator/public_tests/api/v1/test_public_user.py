import pytest
from fastapi.testclient import TestClient

def test_create_user_public(client: TestClient, superuser_token_headers: dict) -> None:
    username = "publicuser42"
    password = "publicpassword42"
    response = client.post(
        "/user/register",
        json={"username": username, "password": password, "nick_name": "PublicNick42"},
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    result = response.json()
    assert result["code"] == 200
    assert result["data"]["username"] == username

def test_search_user_public(client: TestClient, superuser_token_headers: dict) -> None:
    # Search for a different user not used in original test
    username = "publicuser42"
    response = client.get(f"/user/query?username={username}", headers=superuser_token_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)
    found = any(u.get("username") == username for u in data)
    assert found

def test_user_login_public(client: TestClient) -> None:
    username = "publicuser42"
    password = "publicpassword42"
    response = client.post(
        "/user/login", json={"username": username, "password": password}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["code"] == 200
    assert "access_token" in result["data"]

def test_update_password_public(client: TestClient, superuser_token_headers: dict) -> None:
    username = "publicuser42"
    old_password = "publicpassword42"
    new_password = "publicpassword_updated"
    response = client.post(
        "/user/update_password",
        json={"username": username, "old_password": old_password, "new_password": new_password},
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["code"] == 200

def test_delete_user_public(client: TestClient, superuser_token_headers: dict) -> None:
    username = "publicuser42"
    response = client.post(
        "/user/delete",
        json={"username": username},
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["code"] == 200