import pytest
from src.dlv import dlv

def test_retrieves_deeply_nested_value():
    data = {'a': {'b': {'c': 2}}}
    assert dlv(data, 'a.b.c') == 2
    assert dlv(data, ['a', 'b', 'c']) == 2

def test_returns_default_value_if_not_found():
    data = {'a': 1}
    assert dlv(data, 'b', 'default') == 'default'
    assert dlv(data, ['b'], 'default') == 'default'

def test_returns_undefined_when_not_found_and_no_default():
    data = {'a': 1}
    assert dlv(data, 'b') is None

def test_handles_falsy_values():
    data = {'a': False, 'b': 0, 'c': '', 'd': None}
    assert dlv(data, 'a') is False
    assert dlv(data, 'b') == 0
    assert dlv(data, 'c') == ''
    assert dlv(data, 'd') is None

def test_handles_array_indices():
    data = {'a': [1, 2, {'b': 3}]}
    assert dlv(data, 'a.0') == 1
    assert dlv(data, ['a', '1']) == 2
    assert dlv(data, 'a.2.b') == 3
    assert dlv(data, ['a', '2', 'b']) == 3

def test_handles_numeric_keys_as_string_only():
    data = {0: 'a'}
    assert dlv(data, '0') == 'a'
    assert dlv(data, ['0']) == 'a'
    assert dlv([1, 2, 3], '1') == 2

def test_handles_empty_path():
    data = {'a': 1}
    assert dlv(data, '') is None
    assert dlv(data, []) == data

def test_handles_non_object_root():
    assert dlv(None, 'a', 'default') == 'default'
    assert dlv(None, ['a'], 'default') == 'default'
    assert dlv(42, 'a', 'default') == 'default'
    assert dlv('str', ['0'], 'default') == 'default'

def test_should_handle_key_as_object_not_splittable_string():
    # Passing {} as key: should be treated as an empty path (same effect as dlv(obj, []))
    obj = {'a': 1}
    assert dlv(obj, {}, 'not found') == obj

def test_should_handle_arrays_as_objects():
    assert dlv([1, 2, 3], 1, 'x') == [1, 2, 3]
    assert dlv([1, 2, 3], ['1']) == 2

def test_should_treat_keys_with_dots_as_single_key_in_array_form():
    obj = {'a.b': {'c': 1}}
    assert dlv(obj, ['a.b', 'c']) == 1
    assert dlv(obj, 'a.b.c') is None

def test_should_return_default_for_missing_intermediate_object():
    data = {'a': 1}
    assert dlv(data, 'a.b.c', 'foo') == 'foo'
    assert dlv(data, ['a', 'b', 'c'], 'foo') == 'foo'

def test_should_find_value_when_0_is_key():
    data = {'a': {'0': 'test'}}
    assert dlv(data, ['a', '0']) == 'test'
    assert dlv([{'id': 5}], '0.id') == 5

def test_should_work_on_primitive_root_with_empty_path():
    assert dlv(5, [], 'not found') == 5
    assert dlv('abc', [], 'not found') == 'abc'

def test_should_return_default_when_root_is_undefined_null_primitive_and_key_is_not_empty():
    assert dlv(None, ['a'], 'foo') == 'foo'
    assert dlv(None, ['a'], 'foo') == 'foo'
    assert dlv(42, ['a'], 'foo') == 'foo'

def test_should_return_undefined_for_missing_keys_if_no_default():
    assert dlv({}, ['x']) is None
    assert dlv([], ['1']) is None

def test_should_support_symbol_keys():
    class Symbol:
        def __init__(self, desc):
            self.desc = desc
        def __eq__(self, other):
            return type(self) == type(other) and self.desc == getattr(other, 'desc', None)
        def __hash__(self):
            return hash(self.desc)
    s = Symbol('s')
    obj = {s: 42}
    assert dlv(obj, [s], 'foo') == 42

def test_should_return_array_for_empty_string_key_path_on_array():
    assert dlv([4,5,6], '') is None
    assert dlv([4,5,6], []) == [4,5,6]

def test_should_return_default_when_traversing_leaves():
    assert dlv({'a': {'b': 2}}, ['a', 'b', 'c'], 'X') == 'X'
    assert dlv({'a': None}, ['a', 'b'], 'Y') == 'Y'