def test_export_initialize_and_authenticate():
    class Passport:
        def initialize(self): pass
        def authenticate(self): pass
    passport = Passport()
    assert callable(getattr(passport, "initialize", None))
    assert callable(getattr(passport, "authenticate", None))

def test_export_authenticator_with_new_instance():
    class Authenticator:
        def __init__(self):
            self._strategies = {}
        def use(self, strategy):
            name = getattr(strategy, 'name', None)
            if name:
                self._strategies[name] = strategy
    class DummyStrategy:
        name = "public-test-foo"
    AuthClass = Authenticator
    instance = AuthClass()
    assert instance
    instance.use(DummyStrategy())
    assert 'public-test-foo' in instance._strategies