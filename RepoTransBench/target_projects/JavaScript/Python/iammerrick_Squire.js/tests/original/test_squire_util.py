import pytest
from src import squire_node

def test_is_array_function_equivalence():
    # It should return True for lists, False for others
    assert squire_node.isArray([]) is True
    assert squire_node.isArray([1, 2, 3]) is True
    assert squire_node.isArray("not a list") is False
    assert squire_node.isArray({'a': 42}) is False
    assert squire_node.isArray(None) is False

def test_is_function_varieties():
    def f(): pass
    assert squire_node.isFunction(f) is True
    assert squire_node.isFunction(lambda x: x) is True
    assert squire_node.isFunction(print) is True
    assert squire_node.isFunction([1, 2, 3]) is False
    assert squire_node.isFunction({'f': 123}) is False
    assert squire_node.isFunction(None) is False

def test_index_of_various_inputs():
    arr = ['a', 'b', 'c', 'b']
    assert squire_node.indexOf(arr, 'b') == 1
    assert squire_node.indexOf(arr, 'a') == 0
    assert squire_node.indexOf(arr, 'z') == -1
    assert squire_node.indexOf([None, False, 0], 0) == 2

def test_index_of_edge_cases():
    assert squire_node.indexOf([], None) == -1
    assert squire_node.indexOf(None, 123) == -1
    assert squire_node.indexOf("not iterable", 2) == -1

def test_each_array_func():
    arr = [5, 6]
    seen = []
    def f(val, idx):
        seen.append(val + idx)
    squire_node.each(arr, f)
    assert seen == [5, 7]

def test_each_dict_and_object():
    d = {'x': 1, 'y': 2}
    results = []
    def fun(val, key):
        results.append(val + ord(key))
    squire_node.each(d, fun)
    assert len(results) == 2

def test_extend_merges_plain_and_other():
    a = {"foo": 1}
    b = {"bar": 2}
    c = {"baz": 3}
    merged = squire_node.extend(a, b, c)
    assert merged == {"foo": 1, "bar": 2, "baz": 3}

def test_extend_with_empty_and_null():
    d = {'egg': 10}
    squire_node.extend(d, {}, None)
    assert d == {'egg': 10}

def test_clone_dict_and_list_are_copies():
    src = {'a': [1, 2]}
    out = squire_node.clone(src)
    assert out == {'a': [1, 2]}
    assert out is not src
    assert out['a'] == [1, 2]
    # Note: shallow copy

def test_clone_none_and_nonclonables():
    assert squire_node.clone(None) is None
    assert squire_node.clone(9) == 9
    assert squire_node.clone("foo") == "foo"