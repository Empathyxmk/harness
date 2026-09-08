import pytest
from overholt.middleware import HTTPMethodOverrideMiddleware

class DummyApp:
    def __init__(self):
        self.last_environ = None
        self.last_start_response = None

    def __call__(self, environ, start_response):
        self.last_environ = environ
        self.last_start_response = start_response
        start_response("200 OK", [("Content-Type", "text/plain")])
        return [b"response"]

def make_environ(method="POST", query_string="", headers=None):
    environ = {
        "REQUEST_METHOD": method,
        "QUERY_STRING": query_string,
    }
    if headers:
        environ.update(headers)
    return environ

def test_method_override_header():
    app = DummyApp()
    middleware = HTTPMethodOverrideMiddleware(app)
    environ = make_environ(headers={"HTTP_X_HTTP_METHOD_OVERRIDE": "DELETE"})
    called = []
    def start_response(status, headers):
        called.append((status, headers))
    result = list(middleware(environ, start_response))
    assert app.last_environ["REQUEST_METHOD"] == b"DELETE"
    assert "CONTENT_LENGTH" in app.last_environ
    assert result == [b"response"]
    assert called[0][0] == "200 OK"

def test_method_override_querystring():
    app = DummyApp()
    middleware = HTTPMethodOverrideMiddleware(app)
    environ = make_environ(query_string="foo=bar&__METHOD__=PUT")
    called = []
    def start_response(status, headers):
        called.append((status, headers))
    result = list(middleware(environ, start_response))
    assert app.last_environ["REQUEST_METHOD"] == b"PUT"
    assert "CONTENT_LENGTH" in app.last_environ
    assert result == [b"response"]

def test_no_override():
    app = DummyApp()
    middleware = HTTPMethodOverrideMiddleware(app)
    environ = make_environ(method="GET")
    called = []
    def start_response(status, headers):
        called.append((status, headers))
    result = list(middleware(environ, start_response))
    assert app.last_environ["REQUEST_METHOD"] == "GET"
    assert result == [b"response"]

def test_override_with_custom():
    app = DummyApp()
    middleware = HTTPMethodOverrideMiddleware(
        app,
        header_name="X-MY-HEADER",
        querystring_param="__MY_METHOD__",
        allowed_methods=["PUT"]
    )
    environ = make_environ(headers={"HTTP_X_MY_HEADER": "PUT"})
    called = []
    def start_response(status, headers):
        called.append((status, headers))
    result = list(middleware(environ, start_response))
    assert app.last_environ["REQUEST_METHOD"] == b"PUT"

def test_override_not_allowed():
    app = DummyApp()
    middleware = HTTPMethodOverrideMiddleware(app, allowed_methods=["POST"])
    environ = make_environ(headers={"HTTP_X_HTTP_METHOD_OVERRIDE": "PATCH"})
    called = []
    def start_response(status, headers):
        called.append((status, headers))
    result = list(middleware(environ, start_response))
    # Not in allowed methods, should be original
    assert app.last_environ["REQUEST_METHOD"] == "POST"

def test_get_from_querystring_returns_none():
    app = DummyApp()
    middleware = HTTPMethodOverrideMiddleware(app)
    environ = make_environ(query_string="foo=bar")
    assert middleware._get_from_querystring(environ) is None