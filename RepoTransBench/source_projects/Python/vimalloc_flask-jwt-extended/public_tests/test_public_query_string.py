import pytest
from flask import Flask, jsonify

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    JWTManager,
)
from tests.utils import make_headers

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "querysecret"
    app.config["JWT_TOKEN_LOCATION"] = ["query_string"]
    app.config["JWT_QUERY_STRING_NAME"] = "jwt_query"
    JWTManager(app)

    @app.route("/qprotected", methods=["GET"])
    @jwt_required()
    def protected():
        return jsonify(success=True)

    return app

def test_query_string_token(app):
    client = app.test_client()
    with app.test_request_context():
        token = create_access_token("q_user")
    url = "/qprotected?jwt_query={}".format(token)
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.get_json() == {"success": True}