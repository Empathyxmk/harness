from flask_login.test_client import FlaskLoginClient

class DummyUser:
    def __init__(self, id):
        self._id = str(id)
    def get_id(self):
        return self._id

def test_flask_login_client_sets_user_id_public():
    # Simulate minimal Flask-like client structure
    class DummySess(dict):
        def __enter__(self): return self
        def __exit__(self, *a): pass

    class MyClient(FlaskLoginClient):
        def session_transaction(self):
            return self._sess
        def __init__(self, **kwargs):
            self._sess = DummySess()
            super().__init__(**kwargs)

    u = DummyUser("U987")
    client = MyClient(user=u, fresh_login=False)
    assert client._sess["_user_id"] == "U987"
    assert client._sess["_fresh"] is False

def test_flask_login_client_no_user_public():
    # if user is not set, _user_id should not be in session
    class DummySess(dict):
        def __enter__(self): return self
        def __exit__(self, *a): pass

    class MyClient(FlaskLoginClient):
        def session_transaction(self):
            return self._sess
        def __init__(self, **kwargs):
            self._sess = DummySess()
            super().__init__(**kwargs)

    client = MyClient()
    assert "_user_id" not in client._sess
    assert "_fresh" not in client._sess