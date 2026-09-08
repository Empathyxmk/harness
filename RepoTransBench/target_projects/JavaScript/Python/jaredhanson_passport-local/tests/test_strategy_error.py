from passport_local.strategy import Strategy

import pytest

class DummyReq:
    def __init__(self):
        self.body = None
        self.query = None

def test_error_during_verification():
    def verify(username, password, done):
        done(Exception('something went wrong'))
    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {'username': 'johndoe', 'password': 'secret'}
    status, err, _ = strategy.authenticate(req)
    assert status == "error"
    assert isinstance(err, Exception)
    assert str(err) == 'something went wrong'

def test_exception_during_verification():
    def verify(username, password, done):
        raise Exception('something went horribly wrong')
    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {'username': 'johndoe', 'password': 'secret'}
    status, err, _ = strategy.authenticate(req)
    assert status == "error"
    assert isinstance(err, Exception)
    assert str(err) == 'something went horribly wrong'