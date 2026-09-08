import pytest
from src.Store import Store

def test_resolve_non_existent_key_triggers_debug():
    store = Store('adapter', ['foo'])
    assert store.resolve('notfound') is None

def test_register_throws_on_template_validation():
    store = Store('adapter', ['foo'])
    with pytest.raises(Exception, match="must contain"):
        store.register('invalid', {'bar': 123})

def test_valid_registration_and_resolution():
    store = Store('adapter', ['foo'])
    store.register('valid', {'foo': 'bar'})
    assert store.resolve('valid') == {'foo': 'bar'}

def test_validate_returns_false_on_candidate_mismatch():
    store = Store('adapter', ['foo', 'bar'])
    assert store.validate({'foo': 1}) is False

def test_validate_returns_true_on_candidate_match():
    store = Store('adapter', ['foo', 'bar'])
    assert store.validate({'foo': 1, 'bar': 2}) is True