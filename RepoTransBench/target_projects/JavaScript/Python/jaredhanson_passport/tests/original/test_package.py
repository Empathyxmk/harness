def test_expose_singleton_authenticator():
    class Authenticator: pass
    passport = type('passport', (), {'Authenticator': Authenticator})()
    assert isinstance(passport, object)
    assert passport is not None

def test_export_constructors():
    class Authenticator: pass
    class Passport: pass
    class Strategy: pass
    passport = type('passport', (), {'Authenticator': Authenticator, 'Passport': Passport, 'Strategy': Strategy})()
    assert passport.Authenticator is not None
    assert callable(passport.Authenticator)
    assert callable(passport.Strategy)

def test_export_strategies():
    class SessionStrategy: pass
    passport = type('passport', (), {"strategies": type('strategies', (), {'SessionStrategy': SessionStrategy})})()
    assert callable(passport.strategies.SessionStrategy)