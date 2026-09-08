import pytest
from flask import Flask, jsonify, request
from flask_jwt_extended import get_jwt_identity, get_jwt, create_access_token, JWTManager

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "nonprotected"
    JWTManager(app)

    @app.route("/generate", methods=["POST"])
    def generate():
        identity = request.json["id"]
        token = create_access_token(identity)
        return jsonify(token=token)

    @app.route("/nonprotected")
    def np():
        identity = get_jwt_identity()
        data = get_jwt()
        return jsonify(identity=str(identity), token=str(data))

    return app

def test_get_jwt_returns_none(app):
    cli = app.test_client()
    # No JWT provided at all
    response = cli.get("/nonprotected")
    rjson = response.get_json()
    assert rjson["identity"] == "None"
    assert rjson["token"] == "None"