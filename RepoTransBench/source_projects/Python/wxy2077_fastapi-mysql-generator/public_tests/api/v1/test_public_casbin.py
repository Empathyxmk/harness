import pytest
from fastapi.testclient import TestClient

def test_add_policy_public(client: TestClient, superuser_token_headers: dict) -> None:
    # Different user/resource/action for public test
    request_data = {
        "p_type": "p",
        "v0": "public_admin",
        "v1": "/public/data2",
        "v2": "write"
    }
    response = client.post(
        "/casbin/add_policy", json=request_data, headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["code"] == 200

def test_enforce_public(client: TestClient, superuser_token_headers: dict) -> None:
    params = {
        "sub": "public_admin",
        "obj": "/public/data2",
        "act": "write"
    }
    response = client.get(
        "/casbin/enforce",
        params=params,
        headers=superuser_token_headers,
    )
    # Should be true because previous policy was added
    result = response.json()
    assert response.status_code == 200
    assert result["data"] is True

def test_remove_policy_public(client: TestClient, superuser_token_headers: dict) -> None:
    request_data = {
        "p_type": "p",
        "v0": "public_admin",
        "v1": "/public/data2",
        "v2": "write"
    }
    response = client.post(
        "/casbin/remove_policy", json=request_data, headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["code"] == 200

def test_enforce_removed_public(client: TestClient, superuser_token_headers: dict) -> None:
    params = {
        "sub": "public_admin",
        "obj": "/public/data2",
        "act": "write"
    }
    response = client.get(
        "/casbin/enforce",
        params=params,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["data"] is False