from passport_local.strategy import Strategy

class DummyReq:
    def __init__(self):
        self.body = None
        self.query = None

def test_fail_with_custom_bad_request_message_public():
    def verify(username, password, done):
        raise Exception('should not be called - public')
    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {}
    options = {'badRequestMessage': 'Request is malformed (public)'}
    status, info, status_code = strategy.authenticate(req, options)
    assert status == "fail"
    assert info['message'] == 'Request is malformed (public)'
    assert status_code == 400