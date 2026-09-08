import pytest
from flask import Flask, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    JWTManager,
    get_jwt
)
from tests.utils import make_headers

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "addclaims_secret"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims(identity):
        return {"role": "editor", "active": False}

    @app.route("/protected", methods=["GET"])
    @jwt_required()
    def protected():
        claims = get_jwt()
        return jsonify(role=claims.get("role"), active=claims.get("active", None))

    return app

def test_additional_claims_are_included(app):
    test_client = app.test_client()
    with app.test_request_context():
        token = create_access_token("bbrown")
    resp = test_client.get("/protected", headers=make_headers(token))
    assert resp.status_code == 200
    assert resp.get_json() == {"role": "editor", "active": False}