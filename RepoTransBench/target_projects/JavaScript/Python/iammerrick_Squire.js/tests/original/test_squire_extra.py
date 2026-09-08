import pytest
from src import squire_node

def test_util_map_on_list_and_dict():
    arr = [4,5,6]
    def plus1(x): return x+1
    mapped = squire_node.util.map(arr, plus1)
    assert mapped == [5,6,7]
    d = {"x": 2, "y": 3}
    result = squire_node.util.map(d, lambda v, k=None: v*10)
    assert sorted(result) == [20, 30]

def test_util_map_none_and_empty():
    assert squire_node.util.map(None, lambda x: x) == []
    assert squire_node.util.map([], lambda x: x) == []

def test_util_each_iterates_list():
    arr = ["foo", "bar"]
    found = []
    def log(x, i):
        found.append((i, x))
    squire_node.util.each(arr, log)
    assert found == [(0, "foo"), (1, "bar")]

def test_util_each_iterates_dict():
    d = {"p":11, "q":99}
    seen_keys = []
    seen_vals = []
    def f(v, k):
        seen_keys.append(k)
        seen_vals.append(v)
    squire_node.util.each(d, f)
    assert set(seen_keys) == set(["p", "q"])
    assert set(seen_vals) == set([11, 99])

def test_util_some_true_and_false():
    arr = [0, 1, 2]
    assert squire_node.util.some(arr, lambda x: x > 0)
    assert not squire_node.util.some(arr, lambda x: x > 9)
    d = {"a": 11, "b": 0}
    assert squire_node.util.some(d, lambda x: x > 10)
    assert not squire_node.util.some(d, lambda x: x > 100)

def test_util_every_true_and_false():
    arr = [2,2,2]
    assert squire_node.util.every(arr, lambda x: x == 2)
    assert not squire_node.util.every(arr, lambda x: x == 3)
    d = {"foo": 7, "bar": 7}
    assert squire_node.util.every(d, lambda x: x == 7)
    d2 = {"foo": 7, "bar": 8}
    assert not squire_node.util.every(d2, lambda x: x == 7)

def test_util_some_and_every_edge_cases():
    assert squire_node.util.some([], lambda x: x) is False
    assert squire_node.util.some(None, lambda x: x) is False
    assert squire_node.util.every([], lambda x: x) is True
    assert squire_node.util.every(None, lambda x: x) is True