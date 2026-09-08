import pytest
from flask import Flask, render_template_string
from flask_jwt_extended import JWTManager

@pytest.fixture(scope="function")
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "addProc_secret"
    jwt = JWTManager(app)

    @jwt.context_processor
    def context():
        return {"bar": 29}

    return app

def test_context_processor(app):
    app = app
    with app.app_context():
        tpl = "{{ bar }}"
        output = render_template_string(tpl)
        assert output == "29"