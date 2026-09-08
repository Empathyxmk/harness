import pytest
from src.microcache import MicroCache

class TestMicroCache:
    def setup_method(self):
        self.cache = MicroCache()

    def test_should_set_and_get_values(self):
        self.cache.set('a', 123)
        assert self.cache.get('a') == 123
        assert self.cache.contains('a') is True

    def test_should_return_undefined_if_value_not_set(self):
        assert self.cache.get('b') is None
        assert self.cache.contains('b') is False

    def test_should_remove_values(self):
        self.cache.set('key', 'val')
        self.cache.remove('key')
        assert self.cache.get('key') is None
        assert self.cache.contains('key') is False

    def test_should_return_all_values(self):
        self.cache.set('x', 1)
        self.cache.set('y', 2)
        values = self.cache.values()
        assert 'x' in values and values['x'] == 1
        assert 'y' in values and values['y'] == 2

    def test_getset_sets_value_if_absent_and_returns_it(self):
        v = self.cache.getSet('a', 100)
        assert v == 100
        assert self.cache.get('a') == 100

    def test_getset_does_not_overwrite_present_value(self):
        self.cache.set('bar', 77)
        v = self.cache.getSet('bar', 88)
        assert v == 77
        assert self.cache.get('bar') == 77

    def test_getset_sets_using_function_if_value_not_present(self):
        called = {'val': False}
        def func():
            called['val'] = True
            return 42
        v = self.cache.getSet('fn', func)
        assert v == 42
        assert called['val'] is True

    def test_getset_does_not_call_value_function_if_key_is_present(self):
        called = {'val': False}
        def func():
            called['val'] = True
            return 42
        self.cache.set('fn', 43)
        v = self.cache.getSet('fn', func)
        assert v == 43
        assert called['val'] is False

    def test_values_returns_internal_state_object(self):
        self.cache.set('one', 1)
        self.cache.set('two', 2)
        vals = self.cache.values()
        assert isinstance(vals, dict)
        assert vals == {'one': 1, 'two': 2}