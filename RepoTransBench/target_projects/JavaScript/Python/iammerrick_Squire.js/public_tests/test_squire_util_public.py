import pytest
from src import squire_node

def test_is_array_valid_list():
    assert squire_node.isArray([1, 2, 3]) is True

def test_is_array_invalid_object():
    assert squire_node.isArray({'a': 1}) is False

def test_is_function_valid_lambda():
    assert squire_node.isFunction(lambda x: x + 1) is True

def test_is_function_non_function():
    assert squire_node.isFunction(123) is False
    assert squire_node.isFunction([1, 2, 3]) is False

def test_index_of_basic():
    array = [1, 2, 3, 2]
    assert squire_node.indexOf(array, 2) == 1
    assert squire_node.indexOf(array, 3) == 2
    assert squire_node.indexOf(array, 4) == -1

def test_index_of_empty_and_non_list():
    assert squire_node.indexOf([], 1) == -1
    assert squire_node.indexOf(None, 1) == -1
    assert squire_node.indexOf("not a list", 1) == -1

def test_each_array():
    result = []
    def appender(v, i):
        result.append((i, v))
    squire_node.each([5, 6], appender)
    assert result == [(0, 5), (1, 6)]

def test_each_dict():
    data = {"foo": 13, "bar": 15}
    found_keys = []
    found_vals = []
    def f(v, k):
        found_keys.append(k)
        found_vals.append(v)
    squire_node.each(data, f)
    assert "foo" in found_keys or "bar" in found_keys
    assert 13 in found_vals and 15 in found_vals

def test_extend_merges():
    d = {"foo": 1}
    e = {"bar": 2}
    squire_node.extend(d, e)
    assert d["foo"] == 1
    assert d["bar"] == 2

def test_extend_many_sources():
    t = {"x": 1}
    squire_node.extend(t, {'y': 2}, {'z': 3})
    assert t == {"x": 1, "y": 2, "z": 3}

def test_extend_none_source():
    d = {"a": 9}
    squire_node.extend(d, None)
    assert d == {"a": 9}

def test_clone_list_and_dict():
    d = {"a": 1}
    l = [1, 2, 3]
    d2 = squire_node.clone(d)
    l2 = squire_node.clone(l)
    assert d2 == d and d2 is not d
    assert l2 == l and l2 is not l

def test_clone_other_types():
    primitive = 42
    assert squire_node.clone(primitive) == 42
    assert squire_node.clone(None) is None