import pytest
from src.microcache import MicroCache

class TestMicroCachePublic:
    def setup_method(self):
        self.cache = MicroCache()

    def test_should_set_and_get_values_public(self):
        self.cache.set('cat', 789)
        assert self.cache.get('cat') == 789
        assert self.cache.contains('cat') is True

    def test_should_return_undefined_if_value_not_set_public(self):
        assert self.cache.get('dog') is None
        assert self.cache.contains('dog') is False

    def test_should_remove_values_public(self):
        self.cache.set('publicKey', 'publicVal')
        self.cache.remove('publicKey')
        assert self.cache.get('publicKey') is None
        assert self.cache.contains('publicKey') is False

    def test_should_return_all_values_public(self):
        self.cache.set('foo', 10)
        self.cache.set('bar', 20)
        values = self.cache.values()
        assert 'foo' in values and values['foo'] == 10
        assert 'bar' in values and values['bar'] == 20

    def test_getset_sets_value_if_absent_and_returns_it_public(self):
        v = self.cache.getSet('z', 200)
        assert v == 200
        assert self.cache.get('z') == 200

    def test_getset_does_not_overwrite_present_value_public(self):
        self.cache.set('baz', 101)
        v = self.cache.getSet('baz', 303)
        assert v == 101
        assert self.cache.get('baz') == 101

    def test_getset_sets_using_function_if_value_not_present_public(self):
        called = {'val': False}
        def func():
            called['val'] = True
            return 99
        v = self.cache.getSet('cb', func)
        assert v == 99
        assert called['val'] is True

    def test_getset_does_not_call_value_function_if_key_is_present_public(self):
        called = {'val': False}
        def func():
            called['val'] = True
            return 99
        self.cache.set('cb', 55)
        v = self.cache.getSet('cb', func)
        assert v == 55
        assert called['val'] is False

    def test_values_returns_internal_state_object_public(self):
        self.cache.set('alpha', 1234)
        self.cache.set('beta', 5678)
        vals = self.cache.values()
        assert isinstance(vals, dict)
        assert vals == {'alpha': 1234, 'beta': 5678}