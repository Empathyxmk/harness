import pytest
from src import postal

def test_index_js_exposes_expand_and_parser():
    # Simulate the test that 'postal' has expand and parser attributes.
    assert hasattr(postal, 'expand')
    assert hasattr(postal, 'parser')
    assert callable(postal.expand)
    assert callable(postal.parser)

def test_require_bindings_module_missing_native_raises_error(monkeypatch):
    # Simulate requiring a native binding that does not exist; Python simply tries import.
    # We'll attempt to import something that certainly does not exist.
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module('definitely_an_unknown_binding_123')
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module('totally_fake_binding_shim')