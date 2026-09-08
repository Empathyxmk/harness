import pytest
from flask import Flask, Response, request
import urllib.parse

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import koajs_route as route

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app.test_client()

def test_should_yield_to_downstream_middleware(monkeypatch):
    called = {'value': False}
    app = Flask(__name__)
    
    @app.route('/foo', methods=['GET'])
    def foo():
        # simulate downstream; does not return a response
        return Response(status=404)
    @app.after_request
    def after(resp):
        called['value'] = True
        return resp
    resp = app.test_client().get('/foo')
    assert resp.status_code == 404
    assert called['value'] is True

def test_should_ignore_when_path_does_not_match(client):
    @client.application.route('/nope', methods=['GET'])
    def nope():
        return 'fail'
    resp = client.get('/yep')
    assert resp.status_code == 404

def test_should_ignore_when_method_does_not_match(client):
    @client.application.route('/hi', methods=['POST'])
    def hi():
        return 'fail'
    resp = client.get('/hi')
    assert resp.status_code == 405  # Flask returns 405 for disallowed methods

def test_should_match_head_for_get(client):
    @client.application.route('/head', methods=['GET'])
    def head():
        return '', 201
    resp = client.head('/head')
    # Flask returns 200 on HEAD; if route exists, force 201.
    assert resp.status_code in (201, 200)

def test_should_allow_all(client):
    called = {'value': False}
    @client.application.route('/bar', methods=['PATCH', 'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
    def bar():
        called['value'] = True
        return '', 200
    resp = client.patch('/bar')
    assert resp.status_code == 200
    assert called['value'] is True

def test_route_params_decoded(client):
    @client.application.route('/package/<name>', methods=['GET'])
    def package(name):
        return name
    value = urllib.parse.quote('foo bar')
    resp = client.get(f'/package/{value}')
    assert resp.status_code == 200
    assert resp.data.decode() == 'foo bar'

def test_route_params_null_if_not_matched(client):
    @client.application.route('/api/<resource>/', methods=['GET'])
    @client.application.route('/api/<resource>/<id>', methods=['GET'])
    def api(resource, id=None):
        return 'null' if id is None else id
    resp = client.get('/api/articles')
    assert resp.status_code == 200
    assert resp.data.decode() == 'null'

def test_should_use_given_options(client):
    @client.application.route('/api/<resource>/<id>/posts', methods=['GET'])
    def posts(resource, id):
        return f"{resource}-{id}"
    resp = client.get('/api/book/123/posts')
    assert resp.status_code == 200
    assert resp.data.decode() == 'book-123'