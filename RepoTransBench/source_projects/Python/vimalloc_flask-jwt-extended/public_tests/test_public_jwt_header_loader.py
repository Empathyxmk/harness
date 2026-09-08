import pytest
from flask import Flask, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    JWTManager
)
from tests.utils import make_headers, get_jwt_manager

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "headerloader_secret"
    jwt = JWTManager(app)

    @jwt.jwt_header_loader
    def custom_header(identity):
        return {"alg": "HS256", "kid": "public_test"}

    @app.route("/protected", methods=["GET"])
    @jwt_required()
    def protected():
        return jsonify(success="ok")

    return app

def test_custom_header_loader(app):
    jwt = get_jwt_manager(app)

    @jwt.jwt_header_loader
    def custom_header(identity):
        return {"alg": "HS256", "typ": "JWT", "public": "yes"}

    test_client = app.test_client()
    with app.test_request_context():
        token = create_access_token("test_id")
    resp = test_client.get("/protected", headers=make_headers(token))
    assert resp.status_code == 200
    assert resp.get_json()["success"] == "ok"