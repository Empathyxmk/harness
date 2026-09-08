import pytest
from flask import Flask, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, JWTManager
)
from tests.utils import get_jwt_manager, make_headers

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "blocksecret"
    JWTManager(app)
    return app

def test_blocklist_callback(app):
    client = app.test_client()
    jwt = get_jwt_manager(app)
    blocked_tokens = set()

    @jwt.token_in_blocklist_loader
    def check_blocked(jwt_header, jwt_data):
        return jwt_data["sub"] == "to_block"

    @app.route("/protected", methods=["GET"])
    @jwt_required()
    def protected():
        return jsonify(blocked="no")

    with app.test_request_context():
        t1 = create_access_token("not_blocked")
        t2 = create_access_token("to_block")

    # Unblocked user
    resp = client.get("/protected", headers=make_headers(t1))
    assert resp.status_code == 200
    assert resp.get_json()["blocked"] == "no"
    # Blocked user
    resp = client.get("/protected", headers=make_headers(t2))
    assert resp.status_code == 401
    assert resp.get_json()["msg"].lower().startswith("token has been revoked")