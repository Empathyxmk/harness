import io
import sys
import os
import pytest

import flask_jwt_extended
from flask import Flask
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, set_access_cookies, unset_jwt_cookies
)
from datetime import timedelta

@pytest.fixture
def app():
    # Basic JWT app fixture for reuse
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret"
    JWTManager(app)
    return app

def test_implicit_refresh_login_and_protected(monkeypatch):
    from flask import Flask
    from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies, get_jwt, get_jwt_identity
    from flask import jsonify
    from datetime import datetime, timedelta, timezone

    app = Flask(__name__)
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    jwt = JWTManager(app)

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            return response

    @app.route("/login", methods=["POST"])
    def login():
        response = jsonify({"msg": "login successful"})
        access_token = create_access_token(identity="example_user")
        set_access_cookies(response, access_token)
        return response

    @app.route("/logout", methods=["POST"])
    def logout():
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return response

    @app.route("/protected")
    @jwt_required()
    def protected():
        return jsonify(foo="bar")

    client = app.test_client()
    # Login and get cookies set
    resp = client.post("/login")
    assert resp.status_code == 200
    cookies = resp.headers.getlist("Set-Cookie")
    # Access protected
    resp = client.get("/protected", headers={"Cookie": cookies[0].split(";")[0]})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["foo"] == "bar"
    # Test logout
    resp = client.post("/logout")
    assert resp.status_code == 200

def test_example_refresh_tokens():
    from flask import Flask, jsonify
    from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
    from datetime import timedelta
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt = JWTManager(app)

    @app.route("/login", methods=["POST"])
    def login():
        access_token = create_access_token(identity="example_user")
        refresh_token = create_refresh_token(identity="example_user")
        return jsonify(access_token=access_token, refresh_token=refresh_token)

    @app.route("/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh():
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token)

    @app.route("/protected", methods=["GET"])
    @jwt_required()
    def protected():
        return jsonify(foo="bar")

    client = app.test_client()
    # Login to get tokens
    resp = client.post("/login")
    assert resp.status_code == 200
    tokens = resp.get_json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    # Use access token for protected
    resp = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["foo"] == "bar"

    # Use refresh token for /refresh
    resp = client.post(
        "/refresh",
        headers={"Authorization": f"Bearer {tokens['refresh_token']}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data

def test_example_jwt_locations():
    from flask import Flask, jsonify
    from flask_jwt_extended import (
        create_access_token, JWTManager, set_access_cookies, unset_jwt_cookies, jwt_required
    )
    app = Flask(__name__)
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret"
    jwt = JWTManager(app)

    @app.route("/login_without_cookies", methods=["POST"])
    def login_without_cookies():
        access_token = create_access_token(identity="example_user")
        return jsonify(access_token=access_token)

    @app.route("/login_with_cookies", methods=["POST"])
    def login_with_cookies():
        response = jsonify({"msg": "login successful"})
        access_token = create_access_token(identity="example_user")
        set_access_cookies(response, access_token)
        return response

    @app.route("/logout_with_cookies", methods=["POST"])
    def logout_with_cookies():
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return response

    @app.route("/protected", methods=["GET", "POST"])
    @jwt_required()
    def protected():
        return jsonify(foo="bar")

    @app.route("/only_headers")
    @jwt_required(locations=["headers"])
    def only_headers():
        return jsonify(foo="baz")

    client = app.test_client()
    resp = client.post("/login_without_cookies")
    assert resp.status_code == 200
    j = resp.get_json()
    token = j["access_token"]

    # Test protected with headers
    h = {"Authorization": f"Bearer {token}"}
    resp = client.post("/protected", headers=h)
    assert resp.status_code == 200

    # Test /only_headers with headers only (should pass)
    resp = client.get("/only_headers", headers=h)
    assert resp.status_code == 200

    # Test /only_headers without token (should fail)
    resp = client.get("/only_headers")
    assert resp.status_code in (401, 422)

    # Test cookies endpoints
    resp = client.post("/login_with_cookies")
    assert resp.status_code == 200
    cookies_header = resp.headers.getlist("Set-Cookie")[0]
    cookie_name = cookies_header.split("=")[0]
    cookie_value = cookies_header.split("=")[1].split(";")[0]
    cookie = f"{cookie_name}={cookie_value}"

    resp = client.post(
        "/protected", headers={"Cookie": cookie}
    )
    assert resp.status_code == 200

    resp = client.post("/logout_with_cookies", headers={"Cookie": cookie})
    assert resp.status_code == 200

def test_example_loaders():
    from flask import Flask, jsonify
    from flask_jwt_extended import (
        create_access_token, jwt_required, JWTManager
    )

    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret"
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def my_expired_token_callback(jwt_header, jwt_payload):
        return jsonify(code="dave", err="I can't let you do that"), 401

    @app.route("/login", methods=["POST"])
    def login():
        access_token = create_access_token("example_user")
        return jsonify(access_token=access_token)

    @app.route("/protected", methods=["GET"])
    @jwt_required()
    def protected():
        return jsonify(hello="world")

    client = app.test_client()
    resp = client.post("/login")
    assert resp.status_code == 200
    token = resp.get_json()["access_token"]
    resp = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.get_json()["hello"] == "world"

def test_setup_py_version_read_and_long_desc(tmp_path, monkeypatch):
    # Simulates some basic read from setup.py logic
    testfile = tmp_path / "file.py"
    # Writing test version into init file
    package_dir = tmp_path / "flask_jwt_extended"
    package_dir.mkdir()
    initfile = package_dir / "__init__.py"
    initfile.write_text("__version__ = \"1.2.3\"")
    readme = tmp_path / "README.md"
    readme.write_text("# readme stuff\nmore")
    monkeypatch.chdir(tmp_path)
    import re
    import io
    with io.open("flask_jwt_extended/__init__.py", encoding="utf-8") as f:
        version = re.search(r"__version__ = \"(.+)\"", f.read()).group(1)
    assert version == "1.2.3"
    with open("README.md", "r") as f:
        long_description = f.read()
    assert "# readme stuff" in long_description