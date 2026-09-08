import pytest
import math
import datetime
import re
from src.deep_equal import deep_equal

def test_handles_nan_comparisons():
    assert not deep_equal(float('nan'), float('nan'))
    assert not deep_equal(float('nan'), 42)

def test_handles_plus0_minus0_comparisons():
    assert deep_equal(-0.0, +0.0)

def test_handles_regex_equality():
    r1 = re.compile('def', re.G)
    r2 = re.compile('def', re.G)
    r3 = re.compile('def', re.I)
    r4 = re.compile('abc', re.G)
    assert deep_equal(r1, r2)
    assert not deep_equal(r1, r3)
    assert not deep_equal(r1, r4)

def test_handles_date_equality():
    d1 = datetime.datetime(2022, 7, 15)
    d2 = datetime.datetime(2022, 7, 15)
    d3 = datetime.datetime(2023, 7, 15)
    assert deep_equal(d1, d2)
    assert not deep_equal(d1, d3)

def test_handles_different_complex_nested_structures():
    x = {'arr': [5, {'n': 10}, [7, 8]], 'obj': {'a': 9, 'b': [{'f': 20}]}}
    y = {'arr': [5, {'n': 10}, [7, 8]], 'obj': {'a': 9, 'b': [{'f': 20}]}}
    z = {'arr': [5, {'n': 12}, [7, 8]], 'obj': {'a': 9, 'b': [{'f': 20}]}}
    assert deep_equal(x, y)
    assert not deep_equal(x, z)

def test_handles_arguments_objects():
    def bar(x, y, z): return (x, y, z)
    args1 = bar(3, 4, 5)
    args2 = bar(3, 4, 5)
    args3 = bar(7, 8, 9)
    assert deep_equal(args1, args2)
    assert not deep_equal(args1, args3)

def test_different_constructors_with_identical_properties():
    class Apple:
        def __init__(self):
            self.kind = 'fruit'
    class Orange:
        def __init__(self):
            self.kind = 'fruit'
    assert deep_equal(Apple(), Orange())

def test_buffers():
    a = bytes([10, 20, 30])
    b = bytes([10, 20, 30])
    c = bytes([10, 20, 31])
    assert deep_equal(a, b)
    assert not deep_equal(a, c)

def test_maps_and_sets():
    m1 = {10: 'x', 20: 'y'}
    m2 = {10: 'x', 20: 'y'}
    m3 = {10: 'x', 20: 'z'}
    assert deep_equal(m1, m2)
    assert not deep_equal(m1, m3)

    s1 = set([9, 8, 7])
    s2 = set([9, 8, 7])
    s3 = set([9, 8, 6])
    assert deep_equal(s1, s2)
    assert not deep_equal(s1, s3)

def test_functions_are_only_equal_by_reference():
    def foo(): return 2
    def bar(): return 2
    assert deep_equal(foo, foo)
    assert not deep_equal(foo, bar)