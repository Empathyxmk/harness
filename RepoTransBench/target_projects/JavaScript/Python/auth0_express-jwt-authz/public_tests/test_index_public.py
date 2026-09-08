import pytest
from src.express_jwt_authz import express_jwt_authz, InsufficientScopeError

class DummyRes:
    def __init__(self):
        self.statusCode = None
        self.body = None
        self.headers = {}
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

def test_next_called_when_user_has_one_of_expected_scopes():
    req, res, called, next_func = req_res_next()
    req["user"] = {"scope": "read:books download:magazines modify:articles"}
    mw = express_jwt_authz(["download:magazines", "delete:books"])
    mw(req, res, next_func)
    assert called["called"]
    assert called["error"] is None

def test_error_when_user_lacks_required_scopes():
    req, res, called, next_func = req_res_next()
    req["user"] = {"scope": "list:authors read:docs"}
    mw = express_jwt_authz(["download:books"])
    mw(req, res, next_func)
    assert res.statusCode == 403
    assert res.body == "Insufficient scope"
    assert "WWW-Authenticate" in res.headers

def test_accepts_array_user_scope_with_check_all_scopes():
    req, res, called, next_func = req_res_next()
    req["user"] = {"scope": ["publish:news", "edit:news", "share:news"]}
    mw = express_jwt_authz(["publish:news", "edit:news"], {"checkAllScopes": True})
    mw(req, res, next_func)
    assert called["called"]
    assert called["error"] is None

def test_denies_when_not_all_scopes_with_check_all_scopes():
    req, res, called, next_func = req_res_next()
    req["user"] = {"scope": ["manage:users", "edit:accounts"]}
    mw = express_jwt_authz(["manage:users", "admin:users"], {"checkAllScopes": True})
    mw(req, res, next_func)
    assert res.statusCode == 403
    assert res.body == "Insufficient scope"

def test_custom_user_key():
    req, res, called, next_func = req_res_next()
    req["customUser"] = {"scope": "contribute:photos"}
    mw = express_jwt_authz(["contribute:photos"], {"customUserKey": "customUser"})
    mw(req, res, next_func)
    assert called["called"]
    assert called["error"] is None

def test_custom_scope_key():
    req, res, called, next_func = req_res_next()
    req["user"] = {"customScope": "admin:settings"}
    mw = express_jwt_authz(["admin:settings"], {"customScopeKey": "customScope"})
    mw(req, res, next_func)
    assert called["called"]
    assert called["error"] is None

def test_fail_with_error_if_no_user_on_req():
    req, res, called, next_func = req_res_next()
    mw = express_jwt_authz(["edit:profile"], {"failWithError": True})
    mw(req, res, next_func)
    assert called["called"]
    assert called["error"] is not None
    assert getattr(called["error"], "statusCode", None) == 403
    assert getattr(called["error"], "message", str(called["error"])) == "Insufficient scope"

def test_succeed_if_expected_scopes_empty():
    req, res, called, next_func = req_res_next()
    req["user"] = {"scope": "some:random:scope"}
    mw = express_jwt_authz([])
    mw(req, res, next_func)
    assert called["called"]
    assert called["error"] is None

def test_raises_if_expected_scopes_not_array():
    with pytest.raises(TypeError):
        express_jwt_authz("notArray")

def test_error_if_user_scope_not_string_or_array():
    req, res, called, next_func = req_res_next()
    req["user"] = {"scope": 42}
    mw = express_jwt_authz(["write:something"])
    mw(req, res, next_func)
    assert res.statusCode == 403
    assert res.body == "Insufficient scope"