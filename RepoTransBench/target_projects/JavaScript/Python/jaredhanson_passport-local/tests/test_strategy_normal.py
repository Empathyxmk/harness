import pytest

from passport_local.strategy import Strategy

class DummyReq:
    def __init__(self):
        self.body = None
        self.query = None
        self.headers = {}

def test_valid_credentials_in_body():
    def verify(username, password, done):
        if username == 'johndoe' and password == 'secret':
            done(None, {'id': '1234'}, {'scope': 'read'})
            return
        done(None, False)

    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {'username': 'johndoe', 'password': 'secret'}

    status, user, info = strategy.authenticate(req)
    assert status == "success"
    assert isinstance(user, dict)
    assert user['id'] == '1234'
    assert isinstance(info, dict)
    assert info['scope'] == 'read'

def test_valid_credentials_in_query():
    def verify(username, password, done):
        if username == 'johndoe' and password == 'secret':
            done(None, {'id': '1234'}, {'scope': 'read'})
            return
        done(None, False)
    strategy = Strategy(verify)
    req = DummyReq()
    req.query = {'username': 'johndoe', 'password': 'secret'}

    status, user, info = strategy.authenticate(req)
    assert status == "success"
    assert isinstance(user, dict)
    assert user['id'] == '1234'
    assert isinstance(info, dict)
    assert info['scope'] == 'read'

def test_no_body_fails():
    def verify(username, password, done):
        raise Exception('should not be called')
    strategy = Strategy(verify)
    req = DummyReq()
    status, info, status_code = strategy.authenticate(req)
    assert status == "fail"
    assert isinstance(info, dict)
    assert info['message'] == 'Missing credentials'
    assert status_code == 400

def test_no_body_and_no_username_password_fails():
    def verify(username, password, done):
        raise Exception('should not be called')
    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {}
    status, info, status_code = strategy.authenticate(req)
    assert status == "fail"
    assert isinstance(info, dict)
    assert info['message'] == 'Missing credentials'
    assert status_code == 400

def test_no_password_fails():
    def verify(username, password, done):
        raise Exception('should not be called')
    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {'username': 'johndoe'}
    status, info, status_code = strategy.authenticate(req)
    assert status == "fail"
    assert isinstance(info, dict)
    assert info['message'] == 'Missing credentials'
    assert status_code == 400

def test_no_username_fails():
    def verify(username, password, done):
        raise Exception('should not be called')
    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {'password': 'secret'}
    status, info, status_code = strategy.authenticate(req)
    assert status == "fail"
    assert isinstance(info, dict)
    assert info['message'] == 'Missing credentials'
    assert status_code == 400