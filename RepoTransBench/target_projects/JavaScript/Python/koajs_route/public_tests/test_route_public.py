import pytest
from flask import Flask, Response, request
import urllib.parse

def make_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

def test_public_should_yield_to_downstream_middleware():
    called = {'value': False}
    app = make_app()
    @app.route('/public', methods=['GET'])
    def route_public():
        return Response(status=404)
    @app.after_request
    def after(resp):
        called['value'] = True
        return resp
    resp = app.test_client().get('/public')
    assert resp.status_code == 404
    assert called['value'] is True

def test_public_should_ignore_when_path_does_not_match():
    app = make_app()
    @app.route('/notthis', methods=['GET'])
    def notthis():
        return 'fail'
    resp = app.test_client().get('/anotherpath')
    assert resp.status_code == 404

def test_public_should_ignore_when_method_does_not_match():
    app = make_app()
    @app.route('/hi', methods=['PUT'])
    def hi():
        return 'fail'
    resp = app.test_client().get('/hi')
    assert resp.status_code == 405

def test_match_head_for_get_public():
    app = make_app()
    @app.route('/checkhead', methods=['GET'])
    def checkhead():
        return '', 204
    resp = app.test_client().head('/checkhead')
    assert resp.status_code in (204, 200)

def test_allow_all_public():
    called = {'value': False}
    app = make_app()
    @app.route('/pub', methods=['DELETE', 'PATCH', 'GET', 'POST', 'PUT', 'HEAD', 'OPTIONS'])
    def pub():
        called['value'] = True
        return '', 201
    resp = app.test_client().delete('/pub')
    assert resp.status_code == 201
    assert called['value'] is True

def test_route_params_public_should_be_decoded():
    app = make_app()
    @app.route('/city/<name>', methods=['GET'])
    def city(name):
        return name
    value = urllib.parse.quote('new york')
    resp = app.test_client().get(f'/city/{value}')
    assert resp.status_code == 200
    assert resp.data.decode() == 'new york'

def test_route_params_public_should_be_null_if_not_matched():
    app = make_app()
    @app.route('/api2/<type>/', methods=['GET'])
    @app.route('/api2/<type>/<index>', methods=['GET'])
    def api2(type, index=None):
        return 'null' if index is None else index
    resp = app.test_client().get('/api2/widgets')
    assert resp.status_code == 200
    assert resp.data.decode() == 'null'

def test_route_params_public_should_use_given_options():
    app = make_app()
    @app.route('/api2/<category>/<ref>/items', methods=['GET'])
    def items(category, ref):
        return f"{category}:{ref}"
    resp = app.test_client().get('/api2/fruits/999/items')
    assert resp.status_code == 200
    assert resp.data.decode() == 'fruits:999'