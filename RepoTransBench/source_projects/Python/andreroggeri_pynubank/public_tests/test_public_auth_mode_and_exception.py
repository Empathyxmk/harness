import pytest
from pynubank.auth_mode import AuthMode, requires_auth_mode
from pynubank.exception import NuException, NuInvalidAuthenticationMethod, NuMissingCreditCard, NuRequestException
from types import SimpleNamespace

def test_authmode_enum_public():
    assert AuthMode.UNAUTHENTICATED.value == 0
    assert AuthMode.WEB.value != 0
    assert AuthMode.APP.value != AuthMode.WEB.value

def test_requires_auth_mode_success_public():
    class Dummy:
        _auth_mode = AuthMode.APP

        @requires_auth_mode(AuthMode.APP)
        def bar(self):
            return "granted"
    assert Dummy().bar() == "granted"

def test_requires_auth_mode_failure_public():
    class Dummy:
        _auth_mode = AuthMode.WEB

        @requires_auth_mode(AuthMode.APP)
        def bar(self):
            return "refused"

    with pytest.raises(NuInvalidAuthenticationMethod):
        Dummy().bar()

def test_nu_exception_message_public():
    e = NuException("goodbye world")
    assert str(e) == "goodbye world"

def test_nu_invalid_auth_exception_public():
    msg = "Authentication failed"
    exc = NuInvalidAuthenticationMethod(msg)
    assert isinstance(exc, NuException)
    assert msg in str(exc)

def test_nu_missing_credit_card_exception_public():
    e = NuMissingCreditCard()
    assert "credit card" in str(e)
    assert "missing" in str(e)

def fake_response_public():
    resp = SimpleNamespace()
    resp.status_code = 500
    resp.url = "http://other-url"
    return resp

def test_request_exception_public():
    r = fake_response_public()
    exc = NuRequestException(r)
    assert exc.status_code == 500
    assert exc.url == "http://other-url"
    assert str(exc).startswith("The request made failed with HTTP status code")