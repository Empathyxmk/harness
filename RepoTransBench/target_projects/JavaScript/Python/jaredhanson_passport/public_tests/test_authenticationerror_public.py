import pytest

class AuthenticationError(Exception):
    def __init__(self, message, status=401):
        super().__init__(message)
        self.name = "AuthenticationError"
        self.status = status

def test_set_message_and_status_public():
    err = AuthenticationError('public error')
    assert err.name == 'AuthenticationError'
    assert err.args[0] == 'public error'
    assert err.status == 401

def test_custom_status_public():
    err = AuthenticationError('forbidden', 418)
    assert err.status == 418

def test_inherits_from_error_public():
    err = AuthenticationError('bar')
    assert isinstance(err, Exception)