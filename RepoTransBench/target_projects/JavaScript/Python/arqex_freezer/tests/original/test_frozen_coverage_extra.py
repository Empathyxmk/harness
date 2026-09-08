import pytest

from src import frozen

def test_does_not_refreeze_already_frozen_objects():
    obj = {'a': 1}
    froz1 = frozen.freeze(obj)
    froz2 = frozen.freeze(froz1)
    assert froz1 is froz2

def test_tojs_on_primitives():
    assert frozen.toJS(5) == 5
    assert frozen.toJS(None) is None
    assert frozen.toJS(None) is None  # Python has no undefined, use None

def test_equals_custom_equals_method():
    class MyType:
        def equals(self, other):
            return False
    a = MyType()
    b = MyType()
    assert frozen.equals(a, b) is False

def test_equals_for_circular_structures():
    a = {}
    a['self'] = a
    b = {}
    b['self'] = b
    assert frozen.equals(a, b) is True

def test_cyclic_check_with_primitives():
    assert frozen.equals(1, 1) is True