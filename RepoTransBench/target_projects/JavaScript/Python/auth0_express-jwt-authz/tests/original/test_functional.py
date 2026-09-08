import pytest
from src.express_jwt_authz import express_jwt_authz

def call_next(*args, **kwargs):
    call_next.called = True
    call_next.last = args
call_next.called = False
call_next.last = None

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

def test_next_called_immediately_if_expected_scopes_empty():
    req = {'user': {'scope': 'read:user'}}
    called = {'val': False}
    def nxt(*args):
        called['val'] = True
    express_jwt_authz([])(req, {}, nxt)
    assert called['val']

def test_allows_when_expected_scope_in_user_scope_string():
    req = {'user': {'scope': 'read:user write:user'}}
    called = {'val': False}
    def nxt(*args):
        called['val'] = True
    express_jwt_authz(['write:user'])(req, {}, nxt)
    assert called['val']

def test_allows_when_expected_scope_in_user_scope_array():
    req = {'user': {'scope': ['read:user', 'write:user']}}
    called = {'val': False}
    def nxt(*args):
        called['val'] = True
    express_jwt_authz(['write:user'])(req, {}, nxt)
    assert called['val']

def test_all_expected_scopes_present_with_check_all_scopes():
    req = {'user': {'scope': 'read write'}}
    called = {'val': False}
    def nxt(*args):
        called['val'] = True
    express_jwt_authz(['read', 'write'], {'checkAllScopes': True})(req, {}, nxt)
    assert called['val']

def test_denies_when_not_all_expected_scopes_present_and_checkAllScopes_true():
    req = {'user': {'scope': 'read'}}
    res = DummyRes()
    express_jwt_authz(['read', 'write'], {'checkAllScopes': True})(req, res)
    assert res.status_code == 403
    assert res.sent_msg == "Insufficient scope"
    found = any(k == "WWW-Authenticate" and 'scope="read write"' in v for k, v in res.headers)
    assert found

def test_supports_customscopekey_string():
    req = {'user': {'permissions': 'admin'}}
    called = {'val': False}
    def nxt(*args):
        called['val'] = True
    express_jwt_authz(['admin'], {'customScopeKey': 'permissions'})(req, {}, nxt)
    assert called['val']

def test_supports_customscopekey_array():
    req = {'user': {'roles': ['admin', 'manager']}}
    called = {'val': False}
    def nxt(*args):
        called['val'] = True
    express_jwt_authz(['manager'], {'customScopeKey': 'roles'})(req, {}, nxt)
    assert called['val']

def test_supports_customuserkey():
    req = {'account': {'scope': 'foo'}}
    called = {'val': False}
    def nxt(*args):
        called['val'] = True
    express_jwt_authz(['foo'], {'customUserKey': 'account'})(req, {}, nxt)
    assert called['val']

def test_error_if_customuserkey_not_object():
    req = {'notUser': 42}
    res = DummyRes()
    express_jwt_authz(['foo'], {'customUserKey': 'notUser'})(req, res)
    assert res.status_code == 403
    assert res.sent_msg == "Insufficient scope"
    found = any(k == "WWW-Authenticate" and 'scope="foo"' in v for k, v in res.headers)
    assert found

def test_next_called_on_allowed_even_if_failwitherror_true():
    req = {'user': {'scope': 'foo'}}
    called = {'val': False}
    def nxt(*args):
        called['val'] = True
    express_jwt_authz(['foo'], {'failWithError': True})(req, {}, nxt)
    assert called['val']

def test_multiple_scopes_at_least_one_matches():
    req = {'user': {'scope': 'admin operator'}}
    called = {'val': False}
    def nxt(*args):
        called['val'] = True
    express_jwt_authz(['admin', 'user'])(req, {}, nxt)
    assert called['val']