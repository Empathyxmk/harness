import pytest
from pynubank.auth_mode import AuthMode, requires_auth_mode
from pynubank.exception import NuException, NuInvalidAuthenticationMethod, NuMissingCreditCard, NuRequestException
from requests import Response
from types import SimpleNamespace

def test_authmode_enum():
    assert AuthMode.UNAUTHENTICATED.value == 0
    assert AuthMode.WEB.value == 1
    assert AuthMode.APP.value == 2

def test_requires_auth_mode_success():
    class Dummy:
        _auth_mode = AuthMode.WEB

        @requires_auth_mode(AuthMode.WEB)
        def foo(self):
            return "allowed"
    assert Dummy().foo() == "allowed"

def test_requires_auth_mode_failure():
    class Dummy:
        _auth_mode = AuthMode.UNAUTHENTICATED

        @requires_auth_mode(AuthMode.WEB)
        def foo(self):
            return "denied"

    with pytest.raises(NuInvalidAuthenticationMethod):
        Dummy().foo()

def test_nu_exception_message():
    e = NuException("hello")
    assert str(e) == "hello"

def test_nu_invalid_auth_exception():
    msg = "Bad auth"
    exc = NuInvalidAuthenticationMethod(msg)
    assert isinstance(exc, NuException)
    assert msg in str(exc)

def test_nu_missing_credit_card_exception():
    e = NuMissingCreditCard()
    assert "missing credit card" in str(e)

def fake_response():
    resp = SimpleNamespace()
    resp.status_code = 404
    resp.url = "http://test"
    return resp

def test_request_exception():
    r = fake_response()
    exc = NuRequestException(r)
    assert exc.status_code == 404
    assert exc.url == "http://test"
    assert str(exc).startswith("The request made failed with HTTP status code")