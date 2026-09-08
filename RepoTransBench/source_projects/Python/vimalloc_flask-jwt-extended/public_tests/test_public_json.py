import pytest
from flask import Flask
from flask import jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from tests.utils import get_jwt_manager

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "newsecretkey"
    app.config["JWT_TOKEN_LOCATION"] = "json"
    JWTManager(app)

    @app.route("/protected", methods=["POST"])
    @jwt_required()
    def access_protected():
        return jsonify(bar="baz")

    @app.route("/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh_protected():
        return jsonify(bar="baz")

    return app

def test_content_type(app):
    test_client = app.test_client()

    with app.test_request_context():
        access_token = create_access_token("johndoe")
        refresh_token = create_refresh_token("johndoe")

    data = {"access_token": access_token}
    response = test_client.post("/protected", data=data)
    expected_json = {"msg": "Invalid content-type. Must be application/json."}
    assert response.status_code == 401
    assert response.get_json() == expected_json

    data = {"refresh_token": refresh_token}
    response = test_client.post("/refresh", data=data)
    expected_json = {"msg": "Invalid content-type. Must be application/json."}
    assert response.status_code == 401
    assert response.get_json() == expected_json

def test_custom_body_key(app):
    app.config["JWT_JSON_KEY"] = "NewAccess"
    app.config["JWT_REFRESH_JSON_KEY"] = "NewRefresh"
    test_client = app.test_client()

    with app.test_request_context():
        access_token = create_access_token("johndoe")
        refresh_token = create_refresh_token("johndoe")

    # Ensure 'default' keys no longer work
    data = {"access_token": access_token}
    response = test_client.post("/protected", json=data)
    assert response.status_code == 401
    assert response.get_json() == {"msg": 'Missing "NewAccess" key in json data.'}

    data = {"refresh_token": refresh_token}
    response = test_client.post("/refresh", json=data)
    assert response.status_code == 401
    assert response.get_json() == {"msg": 'Missing "NewRefresh" key in json data.'}

    # Ensure new keys do work
    data = {"NewAccess": access_token}
    response = test_client.post("/protected", json=data)
    assert response.status_code == 200
    assert response.get_json() == {"bar": "baz"}

    data = {"NewRefresh": refresh_token}
    response = test_client.post("/refresh", json=data)
    assert response.status_code == 200
    assert response.get_json() == {"bar": "baz"}

def test_missing_keys(app):
    test_client = app.test_client()
    jwtM = get_jwt_manager(app)
    headers = {"content-type": "application/json"}

    # Ensure 'default' no json response
    response = test_client.post("/protected", headers=headers)
    assert response.status_code == 401
    assert response.get_json() == {"msg": 'Missing "access_token" key in json data.'}

    # Test custom no json response
    @jwtM.unauthorized_loader
    def custom_response(err_str):
        return jsonify(bar="baz"), 208

    response = test_client.post("/protected", headers=headers)
    assert response.status_code == 208
    assert response.get_json() == {"bar": "baz"}

def test_defaults(app):
    test_client = app.test_client()

    with app.test_request_context():
        access_token = create_access_token("johndoe")
        refresh_token = create_refresh_token("johndoe")

    data = {"access_token": access_token}
    response = test_client.post("/protected", json=data)
    assert response.status_code == 200
    assert response.get_json() == {"bar": "baz"}

    data = {"refresh_token": refresh_token}
    response = test_client.post("/refresh", json=data)
    assert response.status_code == 200
    assert response.get_json() == {"bar": "baz"}

def test_custom_content_type(app):
    test_client = app.test_client()
    content_type = "application/json; charset=utf-8"

    with app.test_request_context():
        access_token = create_access_token("johndoe")
        refresh_token = create_refresh_token("johndoe")

    data = {"access_token": access_token}
    response = test_client.post("/protected", json=data, content_type=content_type)
    assert response.status_code == 200
    assert response.get_json() == {"bar": "baz"}

    data = {"refresh_token": refresh_token}
    response = test_client.post("/refresh", json=data, content_type=content_type)
    assert response.status_code == 200
    assert response.get_json() == {"bar": "baz"}