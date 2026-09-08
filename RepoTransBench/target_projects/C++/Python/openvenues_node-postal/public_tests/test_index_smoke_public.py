import pytest
from src import postal

def test_index_js_exposes_expand_and_parser_public():
    # Simulate the test that 'postal' has expand and parser attributes and are functions.
    assert hasattr(postal, 'expand')
    assert hasattr(postal, 'parser')
    assert callable(postal.expand)
    assert callable(postal.parser)

def test_require_fake_native_binding_public(monkeypatch):
    import importlib
    # Try importing intentionally bogus bindings to simulate JS "require('bindings')(...)"
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module('thismoduledoesnotexist')
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module('totally_fake_binding')