import pytest
from flask import Flask
from flask import jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from tests.utils import get_jwt_manager
from tests.utils import make_headers

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "yetanothersecret"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims(identity):
        return {"baz": "qux"}

    @app.route("/protectedA", methods=["GET"])
    @jwt_required()
    def protectedA():
        return jsonify(baz="qux")

    @app.route("/protectedB", methods=["GET"])
    @jwt_required(fresh=True)
    def protectedB():
        return jsonify(baz="qux")

    @app.route("/protectedC", methods=["GET"])
    @jwt_required(optional=True)
    def protectedC():
        return jsonify(baz="qux")

    return app

@pytest.mark.parametrize("url", ["/protectedA", "/protectedB", "/protectedC"])
def test_successful_claims_validation(app, url):
    jwt = get_jwt_manager(app)

    @jwt.token_verification_loader
    def claims_verification_callback(jwt_header, jwt_data):
        assert jwt_header["alg"] == "HS256"
        assert jwt_data["sub"] == "janedoe"
        return True

    test_client = app.test_client()
    with app.test_request_context():
        access_token = create_access_token("janedoe", fresh=True)

    response = test_client.get(url, headers=make_headers(access_token))
    assert response.get_json()["baz"] == "qux"
    assert response.status_code == 200

@pytest.mark.parametrize("url", ["/protectedA", "/protectedB", "/protectedC"])
def test_unsuccessful_claims_validation(app, url):
    jwt = get_jwt_manager(app)

    @jwt.token_verification_loader
    def claims_verification_callback(jwt_header, jwt_data):
        assert jwt_header["alg"] == "HS256"
        assert jwt_data["sub"] == "janedoe"
        return False

    test_client = app.test_client()
    with app.test_request_context():
        access_token = create_access_token("janedoe", fresh=True)

    response = test_client.get(url, headers=make_headers(access_token))
    assert response.get_json() == {"msg": "User claims verification failed"}
    assert response.status_code == 400

@pytest.mark.parametrize("url", ["/protectedA", "/protectedB", "/protectedC"])
def test_claims_validation_custom_error(app, url):
    jwt = get_jwt_manager(app)

    @jwt.token_verification_loader
    def claims_verification_callback(jwt_header, jwt_data):
        return False

    @jwt.token_verification_failed_loader
    def custom_error(jwt_header, jwt_data):
        assert jwt_header["alg"] == "HS256"
        assert jwt_data["sub"] == "janedoe"
        return jsonify(msg="claims failed for {}".format(jwt_data["sub"])), 418

    test_client = app.test_client()
    with app.test_request_context():
        access_token = create_access_token("janedoe", fresh=True)

    response = test_client.get(url, headers=make_headers(access_token))
    assert response.get_json() == {"msg": "claims failed for janedoe"}
    assert response.status_code == 418