import pytest
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "optmethod"
    JWTManager(app)

    @app.route("/endpoint", methods=["OPTIONS", "POST"])
    @jwt_required(optional=True)
    def opt():
        return jsonify(answer="options!")

    return app

def test_options_allowed(app):
    client = app.test_client()
    # OPTIONS request should succeed with or without token
    resp = client.options("/endpoint")
    assert resp.status_code in (200, 204)  # allow for either; Flask can return 200 or 204