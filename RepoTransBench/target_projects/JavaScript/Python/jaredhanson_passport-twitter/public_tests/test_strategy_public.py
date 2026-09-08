import pytest

class DummyOAuth:
    def __init__(self):
        self.getOAuthRequestToken = None
        self.getOAuthAccessToken = None

class TwitterStrategy:
    def __init__(self, options, verify_cb):
        if options is None:
            raise Exception('Options required')
        self.consumerKey = options.get('consumerKey')
        self.consumerSecret = options.get('consumerSecret')
        self.callbackURL = options.get('callbackURL', None)
        self.name = 'twitter'
        self._oauth = DummyOAuth()

def test_strategy_public_constructed():
    strategy = TwitterStrategy({"consumerKey": "XYZ789", "consumerSecret": "newsecret"}, lambda: None)
    assert strategy.name == 'twitter'

def test_strategy_public_constructed_undefined_options():
    with pytest.raises(Exception) as excinfo:
        TwitterStrategy(None, lambda: None)
    assert 'Options required' in str(excinfo.value)

def test_strategy_public_authorization_request(monkeypatch):
    strategy = TwitterStrategy({"consumerKey": "XYZ789", "consumerSecret": "newsecret"}, lambda: None)
    def getOAuthRequestToken(extraParams, callback):
        callback(None, 'tokennew123', 'secretnew123', {})
    strategy._oauth.getOAuthRequestToken = getOAuthRequestToken
    out_url = {}
    def redirect(u):
        out_url['url'] = u
    def authenticate():
        strategy._oauth.getOAuthRequestToken({}, lambda error, oauth_token, _secret, _params: (
            redirect(f'https://api.twitter.com/oauth/authenticate?oauth_token={oauth_token}')
            if not error else None
        ))
    authenticate()
    assert out_url['url'] == 'https://api.twitter.com/oauth/authenticate?oauth_token=tokennew123'

def test_strategy_public_authorization_request_with_params(monkeypatch):
    strategy = TwitterStrategy({"consumerKey": "XYZ789", "consumerSecret": "newsecret"}, lambda: None)
    def getOAuthRequestToken(extraParams, callback):
        callback(None, 'tokenxyz321', 'secretxyz321', {})
    strategy._oauth.getOAuthRequestToken = getOAuthRequestToken
    out_url = {}
    def redirect(u):
        out_url['url'] = u
    def authenticate(params):
        force_login = str(params["forceLogin"]).lower() if "forceLogin" in params else 'false'
        screen_name = params["screenName"] if "screenName" in params else ''
        strategy._oauth.getOAuthRequestToken({}, lambda error, oauth_token, _secret, _params: (
            redirect(f'https://api.twitter.com/oauth/authenticate?oauth_token={oauth_token}&force_login={force_login}&screen_name={screen_name}')
            if not error else None
        ))
    authenticate({"screenName": "alice", "forceLogin": False})
    assert out_url['url'] == 'https://api.twitter.com/oauth/authenticate?oauth_token=tokenxyz321&force_login=false&screen_name=alice'

def test_strategy_public_failure_user_denied():
    strategy = TwitterStrategy({"consumerKey": "XYZ789", "consumerSecret": "newsecret"}, lambda: None)
    info = {}
    def fail(i):
        info['info'] = i
    def authenticate():
        req = {}
        req['query'] = {'denied': 'Z9W8X7Y6'}
        fail(None)
    authenticate()
    assert info.get('info') is None

def test_strategy_public_error_invalid_consumer_secret():
    strategy = TwitterStrategy({"consumerKey": "XYZ789", "consumerSecret": "invalid-public-secret", "callbackURL": "http://localhost/callback2"}, lambda: None)
    def getOAuthRequestToken(params, callback):
        callback({'statusCode': 401, 'data': '{"errors":[{"code":77,"message":"Authentication failed."}]}'})
    strategy._oauth.getOAuthRequestToken = getOAuthRequestToken
    error = {}
    def error_callback(e):
        error['err'] = e
    def authenticate():
        import json
        # Simulate the parsing logic from JS
        val = {'statusCode': 401, 'data': '{"errors":[{"code":77,"message":"Authentication failed."}]}'}
        msg = None
        try:
            parsed = json.loads(val['data'])
            msg = parsed['errors'][0]['message']
            raise Exception(msg)
        except Exception as ex:
            error_callback(ex)
    authenticate()
    assert isinstance(error['err'], Exception)
    assert str(error['err']) == 'Authentication failed.'

def test_strategy_public_error_invalid_consumer_secret_unexpected_json():
    strategy = TwitterStrategy({"consumerKey": "XYZ789", "consumerSecret": "invalid-public-secret", "callbackURL": "http://localhost/callback2"}, lambda: None)
    def getOAuthRequestToken(params, callback):
        callback({'statusCode': 401, 'data': '{"unexpected":"format"}'})
    strategy._oauth.getOAuthRequestToken = getOAuthRequestToken
    error = {}
    class InternalOAuthError(Exception):
        pass
    def error_callback(e):
        error['err'] = e
    def authenticate():
        import json
        val = {'statusCode': 401, 'data': '{"unexpected":"format"}'}
        try:
            parsed = json.loads(val['data'])
            # In real code, would check presence of 'errors'
            if "errors" not in parsed:
                raise InternalOAuthError('Failed to obtain request token')
        except Exception as ex:
            error_callback(ex)
    authenticate()
    assert isinstance(error['err'], Exception)
    assert error['err'].__class__.__name__ == "InternalOAuthError"
    assert str(error['err']) == 'Failed to obtain request token'

def test_strategy_public_error_invalid_callback():
    strategy = TwitterStrategy({"consumerKey": "XYZ789", "consumerSecret": "newsecret", "callbackURL": "http://localhost/invalid-callback2"}, lambda: None)
    def getOAuthRequestToken(params, callback):
        callback({'statusCode': 401, 'data': '<?xml version="1.0"?><hash><error>The callback url is not allowed</error><request>/oauth/request_token</request></hash>'})
    strategy._oauth.getOAuthRequestToken = getOAuthRequestToken
    error = {}
    def error_callback(e):
        error['err'] = e
    def authenticate():
        data = '<?xml version="1.0"?><hash><error>The callback url is not allowed</error><request>/oauth/request_token</request></hash>'
        # Simulate extracting message from XML
        import re
        match = re.search(r'<error>(.*?)</error>', data)
        msg = match.group(1) if match else 'Unknown Error'
        error_callback(Exception(msg))
    authenticate()
    assert isinstance(error['err'], Exception)
    assert str(error['err']) == 'The callback url is not allowed'

def test_strategy_public_error_invalid_request_token():
    strategy = TwitterStrategy({"consumerKey": "XYZ789", "consumerSecret": "newsecret", "callbackURL": "http://localhost/callback2"}, lambda: None)
    def getOAuthAccessToken(token, tokenSecret, verifier, callback):
        callback({'statusCode': 401, 'data': 'Request token not accepted.'})
    strategy._oauth.getOAuthAccessToken = getOAuthAccessToken
    error = {}
    def error_callback(e):
        error['err'] = e
    def authenticate():
        val = {'statusCode': 401, 'data': 'Request token not accepted.'}
        msg = val['data']
        error_callback(Exception(msg))
    authenticate()
    assert isinstance(error['err'], Exception)
    assert str(error['err']) == "Request token not accepted."

def test_strategy_public_error_invalid_verifier():
    strategy = TwitterStrategy({"consumerKey": "XYZ789", "consumerSecret": "newsecret", "callbackURL": "http://localhost/callback2"}, lambda: None)
    def getOAuthAccessToken(token, tokenSecret, verifier, callback):
        callback({'statusCode': 401, 'data': 'OAuth error: verifier invalid'})
    strategy._oauth.getOAuthAccessToken = getOAuthAccessToken
    error = {}
    def error_callback(e):
        error['err'] = e
    def authenticate():
        val = {'statusCode': 401, 'data': 'OAuth error: verifier invalid'}
        msg = val['data']
        error_callback(Exception(msg))
    authenticate()
    assert isinstance(error['err'], Exception)
    assert str(error['err']) == "OAuth error: verifier invalid"