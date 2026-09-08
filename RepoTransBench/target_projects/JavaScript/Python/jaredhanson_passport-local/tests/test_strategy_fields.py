from passport_local.strategy import Strategy

class DummyReq:
    def __init__(self):
        self.body = None
        self.query = None

def test_valid_custom_field_names():
    def verify(username, password, done):
        if username == 'johndoe' and password == 'secret':
            done(None, {'id': '1234'}, {'scope': 'read'})
            return
        done(None, False)
    options = {'usernameField': 'userid', 'passwordField': 'passwd'}
    strategy = Strategy(options, verify)
    req = DummyReq()
    req.body = {'userid': 'johndoe', 'passwd': 'secret'}
    status, user, info = strategy.authenticate(req)
    assert status == "success"
    assert user['id'] == '1234'
    assert info['scope'] == 'read'

def test_valid_custom_field_names_object_notation():
    def verify(username, password, done):
        if username == 'johndoe' and password == 'secret':
            done(None, {'id': '1234'}, {'scope': 'read'})
            return
        done(None, False)
    options = {'usernameField': 'user[username]', 'passwordField': 'user[password]'}
    strategy = Strategy(options, verify)
    req = DummyReq()
    req.body = {'user': {'username': 'johndoe', 'password': 'secret'}}
    status, user, info = strategy.authenticate(req)
    assert status == "success"
    assert user['id'] == '1234'
    assert info['scope'] == 'read'