import pytest
from flask import Flask, jsonify
from flask_jwt_extended import (
    jwt_required,
    JWTManager
)

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "getopt_secret"
    JWTManager(app)

    @app.route("/optional", methods=["GET", "POST"])
    @jwt_required(optional=True)
    def optional_view():
        return jsonify(result="optional present")

    return app

def test_optional_methods_public(app):
    client = app.test_client()
    # No token at all
    resp = client.get("/optional")
    assert resp.status_code == 200
    assert resp.get_json() == {"result": "optional present"}
    # POST without token
    resp = client.post("/optional")
    assert resp.status_code == 200
    assert resp.get_json() == {"result": "optional present"}