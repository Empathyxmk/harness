import pytest
from flask import Flask, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, JWTManager
)
from tests.utils import make_headers

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "multiloc_secret"
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]
    app.config["JWT_HEADER_NAME"] = "Auth123"
    app.config["JWT_HEADER_TYPE"] = "JWT"
    app.config["JWT_QUERY_STRING_NAME"] = "myquery"
    JWTManager(app)

    @app.route("/combo", methods=["GET"])
    @jwt_required()
    def combo():
        return jsonify(ok="multi")

    return app

def test_token_header_and_query_locations(app):
    client = app.test_client()
    with app.test_request_context():
        token = create_access_token("multiloc_user")
    # Via header
    resp = client.get("/combo", headers={"Auth123": "JWT {}".format(token)})
    assert resp.status_code == 200
    assert resp.get_json() == {"ok": "multi"}
    # Via query string
    query_url = "/combo?myquery={}".format(token)
    resp = client.get(query_url)
    assert resp.status_code == 200
    assert resp.get_json() == {"ok": "multi"}