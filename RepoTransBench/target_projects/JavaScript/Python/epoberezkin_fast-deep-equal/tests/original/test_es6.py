import pytest

from src.fast_deep_equal.index import fast_deep_equal as equal
import array

def test_compare_maps():
    m1 = dict([('a', 1), ('b', 2)])
    m2 = dict([('a', 1), ('b', 2)])
    m3 = dict([('a', 1), ('b', 3)])
    m4 = dict([('a', 1)])
    m5 = dict([('a', 2), ('c', 3)])
    assert equal(m1, m2) is True
    assert equal(m1, m3) is False
    assert equal(m1, m4) is False
    assert equal(m1, m5) is False

def test_compare_sets():
    s1 = set([1, 2, 3])
    s2 = set([1, 2, 3])
    s3 = set([1, 2])
    s4 = set([3, 2, 1])
    s5 = set([1, 2, 4])
    assert equal(s1, s2) is True
    assert equal(s1, s3) is False
    assert equal(s1, s4) is True
    assert equal(s1, s5) is False

def test_compare_typed_arrays():
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = [1, 2, 4]
    assert equal(a, b) is True
    assert equal(a, c) is False
    d = array.array('H', [1, 2, 3])  # unsigned short
    assert equal(a, d) is False

def test_compare_zero_length_arrays():
    a = []
    b = []
    assert equal(a, b) is True

def test_compare_nested_map_set():
    m1 = {'a': set([1])}
    m2 = {'a': set([1])}
    m3 = {'a': set([2])}
    assert equal(m1, m2) is True
    assert equal(m1, m3) is False

def test_fallback_normal_equal_logic():
    assert equal('a', 'a') is True
    assert equal(1, 2) is False
    assert equal({'x': 1}, {'x': 2}) is False
    assert equal([1, 2], [1, 2]) is True