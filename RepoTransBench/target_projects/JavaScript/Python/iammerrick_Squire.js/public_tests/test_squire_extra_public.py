import pytest
from src import squire_node

def test_util_map_on_list():
    arr = [1, 3, 5]
    def add_1(x):
        return x+1
    mapped = squire_node.util.map(arr, add_1)
    assert mapped == [2, 4, 6]

def test_util_map_on_dict():
    d = {"a": 10, "b": 20}
    found = []
    def fn(v, k=None):
        found.append(v*2)
        return v*2
    results = squire_node.util.map(d, fn)
    # The function should iterate over all values
    assert sorted(results) == [20, 40]
    assert sorted(found) == [20, 40]

def test_util_map_none_returns_empty():
    assert squire_node.util.map(None, lambda x: x) == []

def test_util_each_list():
    arr = [100, 200]
    out = []
    def collect(x, i):
        out.append((i, x))
    squire_node.util.each(arr, collect)
    assert out == [(0, 100), (1, 200)]

def test_util_each_dict():
    d = {"cat": 1, "dog": 2}
    keys = []
    vals = []
    def f(v, k):
        keys.append(k)
        vals.append(v)
    squire_node.util.each(d, f)
    assert sorted(keys) == sorted(list(d.keys()))
    assert sorted(vals) == [1, 2]

def test_util_some_positive_and_negative():
    arr = [0, 0, 3]
    assert squire_node.util.some(arr, lambda x: x > 0) is True
    assert squire_node.util.some(arr, lambda x: x > 3) is False

    d = {"a": 0, "b": 5}
    assert squire_node.util.some(d, lambda x: x > 0) is True
    assert squire_node.util.some(d, lambda x: x > 10) is False

def test_util_some_empty_and_none():
    assert squire_node.util.some([], lambda x: x) is False
    assert squire_node.util.some(None, lambda x: x) is False

def test_util_every_true_and_false():
    arr = [2, 2, 2]
    assert squire_node.util.every(arr, lambda x: x == 2)
    arr2 = [2, 2, 3]
    assert not squire_node.util.every(arr2, lambda x: x == 2)

    d = {"foo": 1, "bar": 1}
    assert squire_node.util.every(d, lambda x: x == 1)
    d2 = {"foo": 1, "bar": 2}
    assert not squire_node.util.every(d2, lambda x: x == 1)

def test_util_every_empty_and_none():
    assert squire_node.util.every([], lambda x: x) is True
    assert squire_node.util.every(None, lambda x: x) is True