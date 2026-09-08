import pytest
from src.get_value import get_value

def test_path_as_array_with_numbers_and_non_strings():
    obj = {'foo': {1: {'bar': 'baz'}}}
    # In python, keys- number: in dicts, so must string-coerce keys
    obj_fixed = {'foo': {'1': {'bar': 'baz'}}}
    assert get_value(obj_fixed, ['foo', 1, 'bar']) == 'baz'

def test_join_segments_with_join_only_first_element():
    def join_only_first(segs):
        return segs[0]
    obj = {'foo': {'bar': 'baz'}}
    options = {'join': join_only_first}
    assert get_value(obj, ['foo', 'bar'], options) == 'baz'

def test_parse_options_separator_when_not_string():
    import re
    obj = {'a': {'b': 'c'}}
    weird_options = {'separator': r'[.]'}  # regex
    assert get_value(obj, 'a.b', weird_options) == 'c'

def test_handle_object_key_being_undefined_returning_options_default():
    obj = {}
    assert get_value(obj, None, {'default': 'zz'}) == 'zz'

def test_return_value_from_root_array_index():
    arr = [1, 2, 3]
    assert get_value(arr, 0) == 1

def test_return_target_path_if_found_when_path_is_array():
    obj = {'foo': {'bar': 'baz'}, 'foo,bar': 'zip'}
    # This triggers direct property lookup when path is ['foo,bar']
    assert get_value(obj, ['foo,bar']) == 'zip'

def test_handle_property_escaping_with_multiple_segments_and_join_function():
    obj = {'a.b.c': {'x': 1}}
    options = {
        'join': lambda segs: '*'.join(segs),
        'separator': '.',
        'joinChar': '*'
    }
    assert get_value(obj, r'a\.b\.c.x', options) == 1

def test_not_treat_a_function_as_object_if_is_valid_filters_out():
    def target(): pass
    options = {'isValid': lambda *a, **k: False, 'default': 'filtered'}
    assert get_value(target, 'someprop', options) == 'filtered'

def test_path_as_undefined():
    obj = {'foo': 1}
    assert get_value(obj, None, {'default': 'none'}) == 'none'

def test_treat_splitchar_as_falsy_and_default_to_dot():
    obj = {'foo': {'bar': 2}}
    options = {'separator': None}
    assert get_value(obj, 'foo.bar', options) == 2

def test_handle_options_not_being_an_object():
    obj = {}
    assert get_value(obj, 'x', 0) == 0
    assert get_value(obj, 'x', False) is False
    assert get_value(obj, 'x', None) is None