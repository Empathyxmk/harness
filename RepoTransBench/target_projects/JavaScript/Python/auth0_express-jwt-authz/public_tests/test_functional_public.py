import pytest
from src.express_jwt_authz import express_jwt_authz, InsufficientScopeError

class DummyRes:
    def __init__(self):
        self.statusCode = None
        self.headers = {}
        self.body = None
    def status(self, code):
        self.statusCode = code
        return self
    def send(self, val):
        self.body = val
        return self
    def append(self, header, value):
        self.headers[header] = value
        return self

@pytest.fixture
def req_res_next():
    req = {}
    res = DummyRes()
    called = {"called": False, "error": None}
    def next_func(err=None):
        called["called"] = True
        called["error"] = err
    return req, res, called, next_func

def test_allow_with_multiple_user_scopes_one_matches():
    req, res, called, next_func = req_res_next()
    req["user"] = {"scope": "export:pdf generate:csv list:files"}
    mw = express_jwt_authz(["generate:csv"])
    mw(req, res, next_func)
    assert called["called"]
    assert called["error"] is None

def test_reject_when_no_scope_matches_expected():
    req, res, called, next_func = req_res_next()
    req["user"] = {"scope": "preview:doc upload:img"}
    mw = express_jwt_authz(["deploy:service"])
    mw(req, res, next_func)
    assert res.statusCode == 403
    assert res.body == "Insufficient scope"

def test_array_in_scope_user_with_check_all_scopes():
    req, res, called, next_func = req_res_next()
    req["user"] = {"scope": ["edit:blog", "update:blog"]}
    mw = express_jwt_authz(["edit:blog", "update:blog"], {"checkAllScopes": True})
    mw(req, res, next_func)
    assert called["called"]

def test_fail_with_error_and_failWithError_scopes_missing():
    req, res, called, next_func = req_res_next()
    req["user"] = {"scope": ["access:repo", "pull:repo"]}
    mw = express_jwt_authz(["release:repo"], {"failWithError": True})
    mw(req, res, next_func)
    assert called["called"]
    assert called["error"] is not None
    assert getattr(called["error"], "statusCode", None) == 403
    assert getattr(called["error"], "message", str(called["error"])) == "Insufficient scope"

def test_respect_custom_scope_key():
    req, res, called, next_func = req_res_next()
    req["user"] = {"myScopes": "accept:invite remove:invite"}
    mw = express_jwt_authz(["accept:invite"], {"customScopeKey": "myScopes"})
    mw(req, res, next_func)
    assert called["called"]
    assert called["error"] is None

def test_respect_custom_user_key():
    req, res, called, next_func = req_res_next()
    req["account"] = {"scope": "claim:rewards"}
    mw = express_jwt_authz(["claim:rewards"], {"customUserKey": "account"})
    mw(req, res, next_func)
    assert called["called"]

def test_next_if_expected_scopes_empty_and_no_user():
    req, res, called, next_func = req_res_next()
    mw = express_jwt_authz([])
    mw(req, res, next_func)
    assert called["called"]
    assert called["error"] is None

def test_error_if_user_scope_null_invalid_type():
    req, res, called, next_func = req_res_next()
    req["user"] = {"scope": {"admin": True}}
    mw = express_jwt_authz(["admin:all"])
    mw(req, res, next_func)
    assert res.statusCode == 403
    assert res.body == "Insufficient scope"

def test_throws_error_if_expected_scopes_not_array():
    with pytest.raises(TypeError):
        express_jwt_authz("foo:bar")

def test_return_error_if_user_key_missing():
    req, res, called, next_func = req_res_next()
    mw = express_jwt_authz(["share:photos"])
    mw(req, res, next_func)
    assert res.statusCode == 403
    assert res.body == "Insufficient scope"