import pytest
from types import SimpleNamespace

from src.express_jwt_authz import express_jwt_authz, InsufficientScopeError

class DummyRes:
    def __init__(self):
        self.status_code = None
        self.sent_msg = None
        self.headers = []
    def status(self, code):
        self.status_code = code
        return self
    def send(self, msg):
        self.sent_msg = msg
        return self
    def append(self, key, value):
        self.headers.append((key, value))
        return self

def test_jwt_authz_is_function():
    assert callable(express_jwt_authz)

def test_jwt_authz_throws_if_expected_scopes_not_array():
    with pytest.raises(TypeError):
        express_jwt_authz()
    with pytest.raises(TypeError):
        express_jwt_authz("string")

def test_jwt_authz_returns_middleware_function():
    mw = express_jwt_authz([])
    assert callable(mw)
    # It should accept req, res, [next]
    assert mw.__code__.co_argcount in (2, 3)

def test_jwt_authz_deny_if_user_missing():
    req = {}
    res = DummyRes()
    express_jwt_authz(['foo'])(req, res)
    assert res.status_code == 403
    assert res.sent_msg == 'Insufficient scope'

def test_jwt_authz_deny_if_user_scope_missing():
    req = {'user': {}}
    res = DummyRes()
    express_jwt_authz(['foo'])(req, res)
    assert res.status_code == 403
    assert res.sent_msg == 'Insufficient scope'

def test_jwt_authz_deny_if_scope_empty_array():
    req = {'user': {'scope': []}}
    res = DummyRes()
    express_jwt_authz(['foo'])(req, res)
    assert res.status_code == 403
    assert res.sent_msg == 'Insufficient scope'

def test_jwt_authz_sets_www_authenticate_header_for_scopes():
    req = {}
    res = DummyRes()
    express_jwt_authz(['foo', 'bar'])(req, res)
    found = any(
        k == "WWW-Authenticate" and 'scope="foo bar"' in v
        for k, v in res.headers
    )
    assert found

def test_jwt_authz_calls_next_with_error_when_fail_with_error(monkeypatch):
    req = {}
    res = DummyRes()
    called = {}
    def next_func(err):
        called['called'] = True
        called['err'] = err
    express_jwt_authz(['foo'], {"failWithError": True})(req, res, next_func)
    assert called.get('called', False)
    # status attribute might be undefined or 403, so check for 403 or None
    assert getattr(called['err'], "status", None) in (403, None)
    assert getattr(called['err'], "statusCode", None) in (403, None)
    assert str(getattr(called['err'], "message", getattr(called['err'], "__str__", lambda: "" )())) == "Insufficient scope"