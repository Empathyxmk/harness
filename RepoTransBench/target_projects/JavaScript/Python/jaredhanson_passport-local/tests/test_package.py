from passport_local import Strategy

def test_exports_strategy_constructor():
    assert callable(Strategy)
    # since our __init__.py exposes only Strategy, we test instance
    s = Strategy(lambda username, password, done=None: None)
    assert isinstance(s, Strategy)