def test_init_sessionmanager_with_alt_string():
    class SessionManager:
        def __init__(self, options=None):
            self._key = options['key'] if options and 'key' in options else "passport"
            self.serialize_user_fn = None
            self.deserialize_user_fn = None

        def serializeUser(self, fn):
            self.serialize_user_fn = fn

        def deserializeUser(self, fn):
            self.deserialize_user_fn = fn

        def serializeUserFunction(self, user, cb):
            self.serialize_user_fn(user, cb)

        def deserializeUserFunction(self, id, cb):
            self.deserialize_user_fn(id, cb)

    sm = SessionManager({"key": "passport-alt"})
    assert sm._key == "passport-alt"

def test_serialize_and_deserialize_user_object_unique_values():
    class SessionManager:
        def __init__(self, options=None):
            self._key = options['key'] if options and 'key' in options else "passport"
            self.serialize_user_fn = None
            self.deserialize_user_fn = None

        def serializeUser(self, fn):
            self.serialize_user_fn = fn

        def deserializeUser(self, fn):
            self.deserialize_user_fn = fn

        def serializeUserFunction(self, user, cb):
            self.serialize_user_fn(user, cb)

        def deserializeUserFunction(self, id, cb):
            self.deserialize_user_fn(id, cb)

    sm = SessionManager({"key": "unique-session"})
    user = {"id": 42, "name": "Zephyr"}
    sm.serializeUser(lambda u, cb: cb(None, u["id"]))
    sm.deserializeUser(lambda id, cb: cb(None, user) if id == 42 else cb(None, False))

    errors = []
    def first_cb(err, result):
        assert err is None
        assert result == 42
        def second_cb(err2, user_result):
            assert err2 is None
            assert user_result == user
        sm.deserializeUserFunction(result, second_cb)
    sm.serializeUserFunction(user, first_cb)