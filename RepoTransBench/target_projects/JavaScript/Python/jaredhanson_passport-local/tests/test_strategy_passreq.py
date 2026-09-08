from passport_local.strategy import Strategy

class DummyReq:
    def __init__(self):
        self.body = None
        self.query = None
        self.headers = {'x-foo': ''}

def test_passing_request_to_verify_callback():
    def verify(req, username, password, done):
        if username == 'johndoe' and password == 'secret':
            done(None, {'id': '1234'}, {'scope': 'read', 'foo': req.headers['x-foo']})
            return
        done(None, False)
    options = {'passReqToCallback': True}
    strategy = Strategy(options, verify)
    req = DummyReq()
    req.headers['x-foo'] = 'hello'
    req.body = {'username': 'johndoe', 'password': 'secret'}
    status, user, info = strategy.authenticate(req)
    assert status == "success"
    assert user['id'] == '1234'
    assert info['scope'] == 'read'
    assert info['foo'] == 'hello'