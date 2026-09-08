import pytest

class Authenticator:
    def __init__(self):
        self._strategies = {}
    def use(self, strategy):
        name = getattr(strategy, "name", None)
        if not name:
            raise Exception("Authentication strategies must have a name")
        self._strategies[name] = strategy
    def authenticate(self, name):
        if name not in self._strategies:
            raise Exception("Unknown authentication strategy")

def test_construct_with_unique_name():
    authenticator = Authenticator()
    assert authenticator

def test_register_new_strategy_with_different_name():
    class DummyStrategy:
        name = "mock-strategy-xyz"
    authenticator = Authenticator()
    authenticator.use(DummyStrategy())
    assert "mock-strategy-xyz" in authenticator._strategies

def test_throw_error_for_unknown_strategy():
    authenticator = Authenticator()
    with pytest.raises(Exception) as e:
        authenticator.authenticate("nonexistent-strategy-789")
    assert "Unknown authentication strategy" in str(e.value)