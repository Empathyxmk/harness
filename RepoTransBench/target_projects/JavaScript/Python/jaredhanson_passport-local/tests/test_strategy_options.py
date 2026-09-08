from passport_local.strategy import Strategy

import pytest
class DummyReq:
    def __init__(self):
        self.body = None
        self.query = None

def test_fail_with_custom_bad_request_message():
    def verify(username, password, done):
        raise Exception('should not be called')
    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {}
    options = {'badRequestMessage': 'Something is wrong with this request'}
    status, info, status_code = strategy.authenticate(req, options)
    assert status == "fail"
    assert isinstance(info, dict)
    assert info['message'] == 'Something is wrong with this request'
    assert status_code == 400