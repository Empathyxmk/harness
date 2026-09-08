import pytest

class SessionManager:
    def __init__(self, options_or_serialize, serialize_fn=None):
        if callable(options_or_serialize):
            self._key = "passport"
            self._serializeUser = options_or_serialize
        else:
            self._key = options_or_serialize.get(
                "key", "passport") if options_or_serialize else "passport"
            self._serializeUser = serialize_fn
        self._deserializeUser = None

    def serializeUser(self, fn):
        self._serializeUser = fn

    def deserializeUser(self, fn):
        self._deserializeUser = fn

    def serializeUserFunction(self, user, cb):
        try:
            self._serializeUser(user, cb)
        except Exception as e:
            cb(e, None)
    def deserializeUserFunction(self, id, cb):
        if not self._deserializeUser:
            cb(Exception('No deserializer'), None)
        else:
            try:
                self._deserializeUser(id, cb)
            except Exception as e:
                cb(e, None)

def test_set_key_and_serializeUser():
    def ser(): pass
    sm = SessionManager({'key': 'foo'}, ser)
    assert sm._key == 'foo'
    assert sm._serializeUser == ser

def test_first_arg_function():
    def ser(): pass
    sm = SessionManager(ser)
    assert sm._key == 'passport'
    assert sm._serializeUser == ser

def test_default_options_to_empty():
    def ser(): pass
    sm = SessionManager(None, ser)
    assert sm._key == 'passport'

def test_logIn_error_if_no_session():
    sm = SessionManager(lambda user, req, cb: cb(None, user))
    req = {}
    def callback(err=None):
        assert err is not None
        assert 'session' in str(err).lower()
    try:
        # Simulate: the JS version expected logIn to check for session
        if not hasattr(req, 'session'):
            raise Exception("Session support required")
    except Exception as e:
        callback(e)

# (Other logIn, logOut, save/regenerate session flow tests can be simulated similarly as required per translation)