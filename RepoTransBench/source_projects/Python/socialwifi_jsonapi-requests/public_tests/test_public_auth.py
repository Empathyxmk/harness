# public test for auth
import pytest
import jsonapi_requests.auth as auth

class DummyConfig:
    AUTH = None

def test_basic_auth_public():
    # Use different values than any in project
    a = auth.BasicAuth("user2", "pass2")
    assert a.username == "user2"
    assert a.password == "pass2"

def test_token_auth_public():
    t = auth.TokenAuth("publictoken")
    assert t.token == "publictoken"

def test_apply_auth_public():
    a = auth.BasicAuth("alice", "secret123")
    config = DummyConfig()
    config.AUTH = a
    assert config.AUTH.username == "alice"
    assert hasattr(config.AUTH, "password")
    assert config.AUTH.password == "secret123"