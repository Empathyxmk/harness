from passport_local.strategy import Strategy

class DummyReq:
    def __init__(self):
        self.body = None
        self.query = None

def test_failing_authentication():
    def verify(username, password, done):
        done(None, False)
    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {'username': 'johndoe', 'password': 'secret'}
    status, info, _ = strategy.authenticate(req)
    assert status == "fail"
    assert info is None

def test_failing_authentication_with_info():
    def verify(username, password, done):
        done(None, False, {'message': 'authentication failed'})
    strategy = Strategy(verify)
    req = DummyReq()
    req.body = {'username': 'johndoe', 'password': 'secret'}
    status, info, _ = strategy.authenticate(req)
    assert status == "fail"
    assert isinstance(info, dict)
    assert info['message'] == 'authentication failed'