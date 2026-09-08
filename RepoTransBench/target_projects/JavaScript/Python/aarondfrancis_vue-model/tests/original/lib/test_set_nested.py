import pytest

from src.lib.set_nested import set_nested

def test_sets_value_deeply_in_object():
    obj = {}
    set_nested(obj, 'a.b.c', 42)
    assert obj['a']['b']['c'] == 42

def test_sets_value_with_custom_separator():
    obj = {}
    set_nested(obj, 'a:b:c', 10, ':')
    assert obj['a']['b']['c'] == 10

def test_overwrites_existing_subobjects():
    obj = {'a': {'b': 5}}
    set_nested(obj, 'a.b.c', 99)
    # Overwrites inner 'b'
    assert obj['a']['b'] == {'c': 99}