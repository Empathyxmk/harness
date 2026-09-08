import pytest
import json

class DummyOAuth:
    def __init__(self):
        self.get = None

class APIError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.name = 'APIError'
        self.code = code
        self.status = 500

class InternalOAuthError(Exception):
    def __init__(self, message, oauthError):
        super().__init__(message)
        self.oauthError = oauthError

class TwitterStrategy:
    def __init__(self, options, verify_cb):
        self.consumerKey = options.get('consumerKey')
        self.consumerSecret = options.get('consumerSecret')
        self.userProfileURL = options.get('userProfileURL', None)
        self.includeEmail = options.get('includeEmail', False)
        self.includeStatus = options.get('includeStatus', True)
        self.includeEntities = options.get('includeEntities', True)
        self.skipExtendedUserProfile = options.get('skipExtendedUserProfile', False)
        self.name = 'twitter'
        self._oauth = DummyOAuth()
        self._verify_cb = verify_cb

    def userProfile(self, token, token_secret, params, done):
        # Simulates async callback as per Node Passport
        try:
            if self.skipExtendedUserProfile:
                prof = type('Profile', (), {})()
                prof.provider = 'twitter'
                prof.id = params.get('user_id')
                prof.username = params.get('screen_name')
                done(None, prof)
                return
            elif self.userProfileURL:
                url = self.userProfileURL + f"?user_id={params['user_id']}"
            else:
                base = "https://api.twitter.com/1.1/account/verify_credentials.json"
                qs = []
                if self.includeEmail:
                    qs.append("include_email=true")
                if not self.includeStatus:
                    qs.append("skip_status=true")
                if not self.includeEntities:
                    qs.append("include_entities=false")
                url = base
                if qs:
                    url += "?" + "&".join(qs)
            def cb_get(error, body, response):
                if error:
                    if hasattr(error, 'statusCode') and hasattr(error, 'data'):
                        bodydict = None
                        try:
                            bodydict = json.loads(error.data)
                            if 'errors' in bodydict:
                                errdata = bodydict['errors'][0]
                                err = APIError(errdata.get("message"), errdata.get("code"))
                                err.status = 500
                                done(err, None)
                                return
                        except Exception:
                            pass
                        done(InternalOAuthError('Failed to fetch user profile', error), None)
                        return
                    done(error, None)
                    return
                try:
                    pdict = json.loads(body)
                    prof = type('Profile', (), {})()
                    prof.provider = 'twitter'
                    prof.id = str(pdict.get('id_str', pdict.get('id')))
                    prof.username = pdict.get('screen_name')
                    prof.displayName = pdict.get('name')
                    prof.photos = []
                    if pdict.get('profile_image_url_https'):
                        Photo = type("Photo", (), {"value": pdict.get('profile_image_url_https')})
                        prof.photos.append(Photo())
                    if pdict.get('email'):
                        Email = type("Email", (), {"value": pdict.get('email')})
                        prof.emails = [Email()]
                    prof._raw = body
                    prof._json = pdict
                    prof._accessLevel = (response or {}).get('headers', {}).get('x-access-level')
                except Exception:
                    done(Exception('Failed to parse user profile'), None)
                    return
                done(None, prof)
            self._oauth.get(url, token, token_secret, cb_get)
        except Exception as ex:
            done(ex, None)

def load_fixture(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        return f.read()

def test_fetched_from_default_endpoint(monkeypatch, tmp_path):
    fname = 'tests/original/fixtures/account/theSeanCook.json'
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret'}, lambda: None)
    def get(url, token, token_secret, callback):
        assert url == 'https://api.twitter.com/1.1/account/verify_credentials.json'
        assert token == 'token'
        assert token_secret == 'token-secret'
        body = load_fixture(fname)
        response = {'headers': {'x-access-level': 'read'}}
        callback(None, body, response)
    strategy._oauth.get = get

    prof = {}
    def done(err, p):
        assert err is None
        prof['profile'] = p
    strategy.userProfile('token', 'token-secret', {'user_id': '6253282'}, done)
    p = prof['profile']
    assert p.provider == 'twitter'
    assert p.id == '38895958'
    assert p.username == 'theSeanCook'
    assert p.displayName == 'Sean Cook'
    assert isinstance(p._raw, str)
    assert isinstance(p._json, dict)
    assert p._accessLevel == 'read'

def test_fetched_from_default_endpoint_with_email(monkeypatch):
    fname = 'tests/original/fixtures/account/theSeanCook.json'
    fname_w_email = 'tests/original/fixtures/account/theSeanCook-include_email.json'
    # Test with 'include_email=true'
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret', 'includeEmail': True}, lambda: None)
    def get(url, token, token_secret, callback):
        expected_url = 'https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true'
        assert url == expected_url
        assert token == 'token'
        assert token_secret == 'token-secret'
        body = load_fixture(fname_w_email)
        response = {'headers': {'x-access-level': 'read'}}
        callback(None, body, response)
    strategy._oauth.get = get

    prof = {}
    def done(err, p):
        assert err is None
        prof['profile'] = p
    strategy.userProfile('token', 'token-secret', {'user_id': '6253282'}, done)
    p = prof['profile']
    assert p.provider == 'twitter'
    assert p.id == '38895958'
    assert p.username == 'theSeanCook'
    assert p.displayName == 'Sean Cook'
    assert isinstance(p._raw, str)
    assert isinstance(p._json, dict)
    assert p._accessLevel == 'read'

def test_fetched_from_default_endpoint_with_status_excluded(monkeypatch):
    fname = 'tests/original/fixtures/account/theSeanCook.json'
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret', 'includeStatus': False}, lambda: None)
    def get(url, token, token_secret, callback):
        expected_url = 'https://api.twitter.com/1.1/account/verify_credentials.json?skip_status=true'
        assert url == expected_url
        assert token == 'token'
        assert token_secret == 'token-secret'
        body = load_fixture(fname)
        response = {'headers': {'x-access-level': 'read'}}
        callback(None, body, response)
    strategy._oauth.get = get

    prof = {}
    def done(err, p):
        assert err is None
        prof['profile'] = p
    strategy.userProfile('token', 'token-secret', {'user_id': '6253282'}, done)
    p = prof['profile']
    assert p.provider == 'twitter'
    assert p.id == '38895958'
    assert p.username == 'theSeanCook'
    assert p.displayName == 'Sean Cook'
    assert isinstance(p._raw, str)
    assert isinstance(p._json, dict)
    assert p._accessLevel == 'read'

def test_fetched_from_default_endpoint_with_entities_excluded(monkeypatch):
    fname = 'tests/original/fixtures/account/theSeanCook.json'
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret', 'includeEntities': False}, lambda: None)
    def get(url, token, token_secret, callback):
        expected_url = 'https://api.twitter.com/1.1/account/verify_credentials.json?include_entities=false'
        assert url == expected_url
        assert token == 'token'
        assert token_secret == 'token-secret'
        body = load_fixture(fname)
        response = {'headers': {'x-access-level': 'read'}}
        callback(None, body, response)
    strategy._oauth.get = get

    prof = {}
    def done(err, p):
        assert err is None
        prof['profile'] = p
    strategy.userProfile('token', 'token-secret', {'user_id': '6253282'}, done)
    p = prof['profile']
    assert p.provider == 'twitter'
    assert p.id == '38895958'
    assert p.username == 'theSeanCook'
    assert p.displayName == 'Sean Cook'
    assert isinstance(p._raw, str)
    assert isinstance(p._json, dict)
    assert p._accessLevel == 'read'

def test_fetched_from_legacy_users_show(monkeypatch):
    # legacy endpoint (feed fixture in-body instead of file for simplicity)
    legacy_json = json.dumps({
        "id_str": "6253282",
        "id": 6253282,
        "screen_name": "twitterapi",
        "name": "Twitter API",
        "profile_image_url_https": "https://si0.twimg.com/profile_images/1438634086/avatar_normal.png",
        "status": {"in_reply_to_status_id_str": None, "id_str":"169566520693882882"},
        "photos": [],
        "description": "The Real Twitter API. I tweet about API changes, service issues and happily answer questions about Twitter and our API. Do not get an answer? It is on my website."
    })
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret', 'userProfileURL': 'https://api.twitter.com/1.1/users/show.json'}, lambda: None)
    def get(url, token, token_secret, callback):
        expected_url = 'https://api.twitter.com/1.1/users/show.json?user_id=6253282'
        assert url == expected_url
        assert token == 'token'
        assert token_secret == 'token-secret'
        body = legacy_json
        response = {'headers': {'x-access-level': 'read'}}
        callback(None, body, response)
    strategy._oauth.get = get

    prof = {}
    def done(err, p):
        assert err is None
        prof['profile'] = p
    strategy.userProfile('token', 'token-secret', {'user_id': '6253282'}, done)
    p = prof['profile']
    assert p.provider == 'twitter'
    assert p.id == '6253282'
    assert p.username == 'twitterapi'
    assert p.displayName == 'Twitter API'
    assert p.photos[0].value == 'https://si0.twimg.com/profile_images/1438634086/avatar_normal.png'
    assert isinstance(p._raw, str)
    assert isinstance(p._json, dict)
    assert p._accessLevel == 'read'

def test_skipping_extended_profile(monkeypatch):
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret', 'skipExtendedUserProfile': True}, lambda: None)
    def get(url, token, token_secret, callback):
        pytest.fail("should not fetch profile")
    strategy._oauth.get = get

    prof = {}
    def done(err, p):
        assert err is None
        prof['profile'] = p
    strategy.userProfile('token', 'token-secret', {"user_id":"1705", "screen_name":"jaredhanson"}, done)
    p = prof['profile']
    assert p.provider == 'twitter'
    assert p.id == '1705'
    assert p.username == 'jaredhanson'
    assert not hasattr(p, '_raw')
    assert not hasattr(p, '_json')

def test_error_invalid_token(monkeypatch):
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret', 'userProfileURL': 'https://api.twitter.com/1.1/users/show.json'}, lambda: None)
    def get(url, token, token_secret, callback):
        body = '{"errors":[{"message":"Invalid or expired token","code":89}]}'
        class OauthError:
            statusCode = 401
            data = body
        callback(OauthError(), None, None)
    strategy._oauth.get = get

    result = {}
    def done(err, p):
        result['err'] = err
        result['profile'] = p
    strategy.userProfile('x-token', 'token-secret', {'user_id': '123'}, done)
    err, profile = result['err'], result['profile']
    assert isinstance(err, APIError)
    assert err.name == "APIError"
    assert err.message == "Invalid or expired token"
    assert err.code == 89
    assert err.status == 500
    assert profile is None

def test_error_malformed_response(monkeypatch):
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret', 'userProfileURL': 'https://api.twitter.com/1.1/users/show.json'}, lambda: None)
    def get(url, token, token_secret, callback):
        body = 'Hello, world.'
        callback(None, body, None)
    strategy._oauth.get = get

    result = {}
    def done(err, p):
        result['err'] = err
        result['profile'] = p
    strategy.userProfile('token', 'token-secret', {'user_id': '123'}, done)
    err, profile = result['err'], result['profile']
    assert isinstance(err, Exception)
    assert str(err) == 'Failed to parse user profile'
    assert profile is None

def test_internal_error(monkeypatch):
    strategy = TwitterStrategy({'consumerKey': 'ABC123', 'consumerSecret': 'secret', 'userProfileURL': 'https://api.twitter.com/1.1/users/show.json'}, lambda: None)
    def get(url, token, token_secret, callback):
        raise Exception('something went wrong')
    strategy._oauth.get = get

    result = {}
    def done(err, p):
        result['err'] = err
        result['profile'] = p
    strategy.userProfile('token', 'token-secret', {'user_id': '123'}, done)
    err, profile = result['err'], result['profile']
    assert isinstance(err, Exception)
    assert err.__class__.__name__ == 'InternalOAuthError'
    assert str(err) == 'Failed to fetch user profile'
    assert hasattr(err, 'oauthError')
    assert err.oauthError.args[0] == 'something went wrong'
    assert profile is None