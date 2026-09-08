import pytest
from flask import Flask, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, decode_token
)
import datetime

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "decodeSecret"
    JWTManager(app)
    return app

def test_decode_token_shows_right_sub(app):
    with app.test_request_context():
        t = create_access_token("decode_user")
        decoded = decode_token(t)
        assert decoded["sub"] == "decode_user"
        assert "exp" in decoded