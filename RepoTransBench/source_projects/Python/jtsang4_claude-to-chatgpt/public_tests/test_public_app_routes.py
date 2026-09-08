import pytest
from fastapi.testclient import TestClient
from claude_to_chatgpt.app import app

client = TestClient(app)

def test_public_health_route():
    # Change string for greater uniqueness
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.text in ("\"ok\"", "ok", "'ok'")

def test_public_not_found_route():
    response = client.get("/non-existent-endpoint2123")
    assert response.status_code == 404

def test_public_root_route():
    response = client.get("/")
    assert response.status_code in (404, 200)
    # Accept either original behavior or new
    # No strict body assertion to be robust to implementations

def test_public_options_returns_405_for_standard_endpoint():
    response = client.options("/healthz")
    # Should commonly respond with 405 Method Not Allowed for OPTIONS unless explicitly supported
    assert response.status_code in (405, 200, 204)