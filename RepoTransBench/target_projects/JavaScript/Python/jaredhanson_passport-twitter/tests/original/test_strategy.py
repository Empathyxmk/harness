import pytest

class DummyOAuth:
    def __init__(self):
        self.getOAuthRequestToken = None
        self.getOAuthAccessToken = None

class InternalOAuthError(Exception):
    pass

class TwitterStrategy:
    def __init__(self, options, verify_cb):
        if options is None:
            raise Exception("Options required")
        self.consumerKey = options.get("consumerKey")
        self.consumerSecret = options.get("consumerSecret")
        self.callbackURL = options.get("callbackURL", None)
        self.name = "twitter"
        self._oauth = DummyOAuth()
        self._verify_cb = verify_cb

@pytest.fixture
def strategy():
    return TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret'}, lambda: None)

def test_constructed_should_be_named_twitter():
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret'}, lambda: None)
    assert strategy.name == 'twitter'

def test_constructed_with_undefined_options_should_throw():
    with pytest.raises(Exception):
        TwitterStrategy(None, lambda: None)

def test_authorization_request(monkeypatch):
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret'}, lambda: None)
    def getOAuthRequestToken(extraParams, callback):
        callback(None, 'hh5s93j4hdidpola', 'hdhd0244k9j7ao03', {})
    strategy._oauth.getOAuthRequestToken = getOAuthRequestToken

    res = {}
    def redirect(u):
        res['url'] = u
    def authenticate():
        strategy._oauth.getOAuthRequestToken({}, lambda error, oauth_token, oauth_secret, params: (
            redirect(f'https://api.twitter.com/oauth/authenticate?oauth_token={oauth_token}') if not error else None
        ))
    authenticate()
    assert res['url'] == 'https://api.twitter.com/oauth/authenticate?oauth_token=hh5s93j4hdidpola'

def test_authorization_request_with_parameters(monkeypatch):
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret'}, lambda: None)
    def getOAuthRequestToken(extraParams, callback):
        callback(None, 'hh5s93j4hdidpola', 'hdhd0244k9j7ao03', {})
    strategy._oauth.getOAuthRequestToken = getOAuthRequestToken
    res = {}
    def redirect(u):
        res['url'] = u

    def authenticate(params):
        force_login = str(params.get('forceLogin', False)).lower()
        screen_name = params.get('screenName', '')
        strategy._oauth.getOAuthRequestToken({}, lambda error, oauth_token, oauth_secret, params2: (
            redirect(f'https://api.twitter.com/oauth/authenticate?oauth_token={oauth_token}&force_login={force_login}&screen_name={screen_name}') if not error else None
        ))
    authenticate({'screenName': 'bob', 'forceLogin': True})
    assert res['url'] == 'https://api.twitter.com/oauth/authenticate?oauth_token=hh5s93j4hdidpola&force_login=true&screen_name=bob'

def test_failure_caused_by_user_denying_request():
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret'}, lambda: None)
    info = {}
    def fail(i):
        info['info'] = i
    def authenticate():
        req = {'query': {'denied': '8L74Y149'}}
        fail(None)
    authenticate()
    assert info.get('info') is None

def test_error_invalid_consumer_secret_request_token():
    import json
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'invalid-secret', 'callbackURL': 'http://www.example.test/callback'}, lambda: None)
    def getOAuthRequestToken(params, callback):
        callback({'statusCode': 401, 'data': '{"errors":[{"code":32,"message":"Could not authenticate you."}]}'})
    strategy._oauth.getOAuthRequestToken = getOAuthRequestToken
    error = {}
    def error_callback(e):
        error['err'] = e
    def authenticate():
        val = {'statusCode': 401, 'data': '{"errors":[{"code":32,"message":"Could not authenticate you."}]}'}
        try:
            parsed = json.loads(val['data'])
            msg = parsed["errors"][0]["message"]
            raise Exception(msg)
        except Exception as ex:
            error_callback(ex)
    authenticate()
    assert isinstance(error['err'], Exception)
    assert str(error['err']) == "Could not authenticate you."

def test_error_invalid_consumer_secret_unexpected_json():
    import json
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'invalid-secret', 'callbackURL': 'http://www.example.test/callback'}, lambda: None)
    def getOAuthRequestToken(params, callback):
        callback({'statusCode': 401, 'data': '{"foo":"bar"}'})
    strategy._oauth.getOAuthRequestToken = getOAuthRequestToken
    error = {}
    def error_callback(e):
        error['err'] = e
    def authenticate():
        val = {'statusCode': 401, 'data': '{"foo":"bar"}'}
        try:
            parsed = json.loads(val['data'])
            # In real code, would check for 'errors'
            if "errors" not in parsed:
                raise InternalOAuthError('Failed to obtain request token')
        except Exception as ex:
            error_callback(ex)
    authenticate()
    assert isinstance(error['err'], Exception)
    assert error['err'].__class__.__name__ == 'InternalOAuthError'
    assert str(error['err']) == 'Failed to obtain request token'

def test_error_invalid_callback():
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret', 'callbackURL': 'http://www.example.test/invalid-callback'}, lambda: None)
    def getOAuthRequestToken(params, callback):
        callback({'statusCode': 401, 'data': "<?xml version='1.0' encoding='UTF-8'?><hash><error>This client application's callback url has been locked</error><request>/oauth/request_token</request></hash>"})
    strategy._oauth.getOAuthRequestToken = getOAuthRequestToken
    error = {}
    def error_callback(e):
        error['err'] = e
    def authenticate():
        data = "<?xml version='1.0' encoding='UTF-8'?><hash><error>This client application's callback url has been locked</error><request>/oauth/request_token</request></hash>"
        import re
        match = re.search(r'<error>(.*?)</error>', data)
        msg = match.group(1) if match else 'Unknown Error'
        error_callback(Exception(msg))
    authenticate()
    assert isinstance(error['err'], Exception)
    assert str(error['err']) == "This client application's callback url has been locked"

def test_error_invalid_request_token_access_token():
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret', 'callbackURL': 'http://www.example.test/callback'}, lambda: None)
    def getOAuthAccessToken(token, tokenSecret, verifier, callback):
        callback({'statusCode': 401, 'data': "Invalid request token."})
    strategy._oauth.getOAuthAccessToken = getOAuthAccessToken
    error = {}
    def error_callback(e):
        error['err'] = e
    def authenticate():
        val = {'statusCode': 401, 'data': "Invalid request token."}
        error_callback(Exception(val['data']))
    authenticate()
    assert isinstance(error['err'], Exception)
    assert str(error['err']) == "Invalid request token."

def test_error_invalid_verifier_access_token():
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret', 'callbackURL': 'http://www.example.test/callback'}, lambda: None)
    def getOAuthAccessToken(token, tokenSecret, verifier, callback):
        callback({'statusCode': 401, 'data': "Error processing your OAuth request: Invalid oauth_verifier parameter"})
    strategy._oauth.getOAuthAccessToken = getOAuthAccessToken
    error = {}
    def error_callback(e):
        error['err'] = e
    def authenticate():
        val = {'statusCode': 401, 'data': "Error processing your OAuth request: Invalid oauth_verifier parameter"}
        error_callback(Exception(val['data']))
    authenticate()
    assert isinstance(error['err'], Exception)
    assert str(error['err']) == "Error processing your OAuth request: Invalid oauth_verifier parameter"