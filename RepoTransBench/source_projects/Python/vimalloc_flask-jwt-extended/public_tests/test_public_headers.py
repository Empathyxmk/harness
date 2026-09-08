import pytest
from flask import Flask, jsonify

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    JWTManager,
)
from tests.utils import get_jwt_manager, make_headers

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "headersecret"
    app.config["JWT_HEADER_NAME"] = "X-Custom-Auth"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    JWTManager(app)

    @app.route("/protected", methods=["GET"])
    @jwt_required()
    def protected():
        return jsonify(custom="header")

    return app

def test_custom_header(app):
    test_client = app.test_client()
    with app.test_request_context():
        token = create_access_token("alice")

    headers = {"X-Custom-Auth": "Bearer {}".format(token)}
    resp = test_client.get("/protected", headers=headers)
    assert resp.status_code == 200
    assert resp.get_json() == {"custom": "header"}

def test_invalid_header_type(app):
    test_client = app.test_client()
    with app.test_request_context():
        token = create_access_token("alice")
    headers = {"X-Custom-Auth": "Token {}".format(token)}
    resp = test_client.get("/protected", headers=headers)
    assert resp.status_code == 401
    assert resp.get_json()["msg"].lower().startswith("invalid")

def test_missing_custom_header(app):
    test_client = app.test_client()
    resp = test_client.get("/protected")
    assert resp.status_code == 401
    assert resp.get_json()["msg"].startswith("Missing 'X-Custom-Auth' Header")