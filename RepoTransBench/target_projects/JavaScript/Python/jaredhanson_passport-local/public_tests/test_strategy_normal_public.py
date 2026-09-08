from passport_local.strategy import Strategy

import pytest

class DummyReq:
    def __init__(self):
        self.body = None
        self.query = None

def test_valid_credentials_in_body_public():
    def verify(username, password, done):
        if username == 'janedoe' and password == 'hunter2':
            done(None, {'id': '5678'}, {'scope': 'write'})
            return
        done(None, False)
    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {'username': 'janedoe', 'password': 'hunter2'}
    status, user, info = strategy.authenticate(req)
    assert status == "success"
    assert user['id'] == '5678'
    assert info['scope'] == 'write'

def test_valid_credentials_in_query_public():
    def verify(username, password, done):
        if username == 'janedoe' and password == 'hunter2':
            done(None, {'id': '5678'}, {'scope': 'write'})
            return
        done(None, False)
    strategy = Strategy(verify)
    req = DummyReq()
    req.query = {'username': 'janedoe', 'password': 'hunter2'}
    status, user, info = strategy.authenticate(req)
    assert status == "success"
    assert user['id'] == '5678'
    assert info['scope'] == 'write'

def test_no_body_public():
    def verify(username, password, done):
        raise Exception('should not be called - public')
    strategy = Strategy(verify)
    req = DummyReq()
    status, info, status_code = strategy.authenticate(req)
    assert status == "fail"
    assert info['message'] == 'Missing credentials'
    assert status_code == 400

def test_no_body_and_no_username_password_public():
    def verify(username, password, done):
        raise Exception('should not be called - public')
    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {}
    status, info, status_code = strategy.authenticate(req)
    assert status == "fail"
    assert info['message'] == 'Missing credentials'
    assert status_code == 400

def test_no_password_public():
    def verify(username, password, done):
        raise Exception('should not be called - public')
    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {'username': 'janedoe'}
    status, info, status_code = strategy.authenticate(req)
    assert status == "fail"
    assert info['message'] == 'Missing credentials'
    assert status_code == 400

def test_no_username_public():
    def verify(username, password, done):
        raise Exception('should not be called - public')
    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {'password': 'hunter2'}
    status, info, status_code = strategy.authenticate(req)
    assert status == "fail"
    assert info['message'] == 'Missing credentials'
    assert status_code == 400