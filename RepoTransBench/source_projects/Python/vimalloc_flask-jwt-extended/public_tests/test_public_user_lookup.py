import pytest
from flask import Flask
from flask import jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import get_current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from tests.utils import get_jwt_manager
from tests.utils import make_headers

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "anothersecret"
    JWTManager(app)

    @app.route("/lookup1", methods=["GET"])
    @jwt_required()
    def lookup1():
        try:
            return jsonify(bar=get_current_user()["email"])
        except RuntimeError as e:
            return jsonify(warning=str(e))

    @app.route("/lookup2", methods=["GET"])
    @jwt_required()
    def lookup2():
        try:
            return jsonify(bar=current_user["email"])
        except RuntimeError as e:
            return jsonify(warning=str(e))

    return app

@pytest.mark.parametrize("url", ["/lookup1", "/lookup2"])
def test_no_user_lookup_loader_specified(app, url):
    test_client = app.test_client()
    with app.test_request_context():
        access_token = create_access_token("janedoe")

    response = test_client.get(url, headers=make_headers(access_token))
    assert "@jwt.user_lookup_loader" in response.get_json()["warning"]

@pytest.mark.parametrize("url", ["/lookup1", "/lookup2"])
def test_load_valid_user(app, url):
    jwt = get_jwt_manager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        return {"email": jwt_data["sub"] + "@mail.com"}

    test_client = app.test_client()
    with app.test_request_context():
        access_token = create_access_token("janedoe")

    response = test_client.get(url, headers=make_headers(access_token))
    assert response.status_code == 200
    assert response.get_json() == {"bar": "janedoe@mail.com"}

@pytest.mark.parametrize("url", ["/lookup1", "/lookup2"])
def test_load_invalid_user(app, url):
    jwt = get_jwt_manager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        return None

    test_client = app.test_client()
    with app.test_request_context():
        access_token = create_access_token("janedoe")

    response = test_client.get(url, headers=make_headers(access_token))
    assert response.status_code == 401
    assert response.get_json() == {"msg": "Error loading the user janedoe"}

@pytest.mark.parametrize("url", ["/lookup1", "/lookup2"])
def test_custom_user_lookup_errors(app, url):
    jwt = get_jwt_manager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        return None

    @jwt.user_lookup_error_loader
    def user_lookup_error(jwt_header, jwt_data):
        assert jwt_header["alg"] == "HS256"
        assert jwt_data["sub"] == "janedoe"
        return jsonify(bar="baz"), 202

    test_client = app.test_client()
    with app.test_request_context():
        access_token = create_access_token("janedoe")

    response = test_client.get(url, headers=make_headers(access_token))
    assert response.status_code == 202
    assert response.get_json() == {"bar": "baz"}