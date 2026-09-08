import pytest
from unittest import mock

import types

@pytest.fixture
def mkapp():
    # Dynamically create a Flask-like app for test scaffold
    from flask import Flask, jsonify
    app = Flask(__name__)
    @app.route('/api')
    def api():
        return jsonify(success=True)
    return app

def test_get_api_returns_json(mkapp):
    # Use Flask test client (simulating supertest/express)
    app = mkapp
    client = app.test_client()
    res = client.get('/api')
    assert res.status_code == 200
    assert 'application/json' in res.content_type
    assert res.json['success'] is True