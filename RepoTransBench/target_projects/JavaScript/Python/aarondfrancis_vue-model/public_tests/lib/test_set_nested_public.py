import pytest

from src.lib.set_nested import set_nested

def test_sets_a_simple_different_key_value():
    obj = {}
    set_nested(obj, 'alpha', 42)
    assert obj['alpha'] == 42

def test_sets_a_nested_property_with_another_path():
    obj = {}
    set_nested(obj, 'x.y.z', 'test')
    assert obj['x']['y']['z'] == 'test'

def test_does_not_overwrite_intermediate_objects_if_already_set_with_different_vals():
    obj = {'n': {'p': 11}}
    set_nested(obj, 'n.q', 22)
    assert obj['n']['p'] == 11
    assert obj['n']['q'] == 22

def test_sets_deep_property_with_array_index():
    obj = {}
    set_nested(obj, 'arr.0.a', 'first')
    assert isinstance(obj['arr'], list)
    assert obj['arr'][0]['a'] == 'first'