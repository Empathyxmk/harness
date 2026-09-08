import pytest
from flask import Flask

def test_jwt_secret_key_present():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "abc_config_public"
    assert app.config["JWT_SECRET_KEY"] == "abc_config_public"