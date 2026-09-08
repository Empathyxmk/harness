import pytest
from src.dlv import dlv

def test_retrieves_deeply_nested_value():
    data = {'x': {'y': {'z': 99}}}
    assert dlv(data, 'x.y.z') == 99
    assert dlv(data, ['x','y','z']) == 99

def test_returns_default_value_if_not_found():
    data = {'foo': 9}
    assert dlv(data, 'bar', 42) == 42
    assert dlv(data, ['bar'], None) is None

def test_returns_undefined_when_not_found_and_no_default():
    data = {'hello': 'world'}
    assert dlv(data, 'absent') is None

def test_handles_falsy_values():
    data = {'a': '', 'b': False, 'c': 0, 'd': None}
    assert dlv(data, 'a') == ''
    assert dlv(data, 'b') is False
    assert dlv(data, 'c') == 0
    assert dlv(data, 'd') is None

def test_handles_array_indices():
    data = {'arr': [10, 20, {'x': 30}]}
    assert dlv(data, 'arr.0') == 10
    assert dlv(data, ['arr','1']) == 20
    assert dlv(data, 'arr.2.x') == 30
    assert dlv(data, ['arr','2','x']) == 30

def test_handles_numeric_keys_as_string_only():
    data = {1: 'b'}
    assert dlv(data, '1') == 'b'
    assert dlv(data, ['1']) == 'b'
    assert dlv([5,6,7], '2') == 7

def test_handles_empty_path():
    data = {'foo':2}
    assert dlv(data, '') is None
    assert dlv(data, []) == data

def test_handles_non_object_root():
    assert dlv(None, 'q', 'fallback') == 'fallback'
    assert dlv(None, ['x'], 'abc') == 'abc'
    assert dlv(100, 'y', 'red') == 'red'
    assert dlv('hello', ['0'], 'zero') == 'zero'

def test_should_handle_key_as_object_not_splittable_string():
    obj = {'b': 2}
    assert dlv(obj, {}, 'missing') == obj

def test_should_handle_arrays_as_objects():
    assert dlv([9,8,7], 2, 'none') == [9,8,7]
    assert dlv([3,4,5], ['2']) == 5

def test_should_treat_keys_with_dots_as_single_key_in_array_form():
    obj = {'x.y': {'w': 10}}
    assert dlv(obj, ['x.y', 'w']) == 10
    assert dlv(obj, 'x.y.w') is None

def test_should_return_default_for_missing_intermediate_object():
    data = {'b': 2}
    assert dlv(data, 'b.z.y', 'out') == 'out'
    assert dlv(data, ['b', 'z', 'y'], 'miss') == 'miss'

def test_should_find_value_when_0_is_key():
    data = {'b': {'0': 'value0'}}
    assert dlv(data, ['b', '0']) == 'value0'
    assert dlv([{'name': 'a'}], '0.name') == 'a'

def test_should_work_on_primitive_root_with_empty_path():
    assert dlv(True, [], 'no') is True
    assert dlv('xyz', [], 'no') == 'xyz'

def test_should_return_default_when_root_is_undefined_null_primitive_and_key_is_not_empty():
    assert dlv(None, ['baz'], 'qux') == 'qux'
    assert dlv(None, ['baz'], 777) == 777
    assert dlv(1, ['foo'], False) is False

def test_should_return_undefined_for_missing_keys_if_no_default():
    assert dlv({}, ['absent']) is None
    assert dlv([], ['4']) is None

def test_should_support_symbol_keys():
    class Symbol:
        def __init__(self, desc):
            self.desc = desc
        def __eq__(self, other):
            return type(self) == type(other) and self.desc == getattr(other, 'desc', None)
        def __hash__(self):
            return hash(self.desc)
    s = Symbol('another')
    obj = {s: 7}
    assert dlv(obj, [s], 11) == 7

def test_should_return_array_for_empty_string_key_path_on_array():
    assert dlv([9,8,7], '') is None
    assert dlv([9,8,7], []) == [9,8,7]

def test_should_return_default_when_traversing_leaves():
    assert dlv({'b': {'c': 5}}, ['b','c','d'], 'Leaf') == 'Leaf'
    assert dlv({'b': None}, ['b','z'], 'Done') == 'Done'