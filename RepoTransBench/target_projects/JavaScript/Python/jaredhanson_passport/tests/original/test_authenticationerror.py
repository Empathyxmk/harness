import pytest

class AuthenticationError(Exception):
    def __init__(self, message, status=401):
        super().__init__(message)
        self.name = "AuthenticationError"
        self.status = status

def test_should_set_message_and_status():
    err = AuthenticationError('failmessage')
    assert err.name == 'AuthenticationError'
    assert err.args[0] == 'failmessage'
    assert err.status == 401

def test_should_allow_custom_status():
    err = AuthenticationError('err', 403)
    assert err.status == 403

def test_should_inherit_from_error():
    err = AuthenticationError('foo')
    assert isinstance(err, Exception)