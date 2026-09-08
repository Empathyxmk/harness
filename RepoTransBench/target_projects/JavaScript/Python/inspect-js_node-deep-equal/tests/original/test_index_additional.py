import pytest
import math
import datetime
import re
from src.deep_equal import deep_equal

def test_handles_nan_comparisons():
    assert not deep_equal(float('nan'), float('nan'))
    assert not deep_equal(float('nan'), 5)

def test_handles_plus0_minus0_comparisons():
    assert deep_equal(+0.0, -0.0)

def test_handles_regex_equality():
    r1 = re.compile('abc', re.I)
    r2 = re.compile('abc', re.I)
    r3 = re.compile('abc')
    r4 = re.compile('def', re.I)
    assert deep_equal(r1, r2)
    assert not deep_equal(r1, r3)
    assert not deep_equal(r1, r4)

def test_handles_date_equality():
    d1 = datetime.datetime(2023, 1, 1)
    d2 = datetime.datetime(2023, 1, 1)
    d3 = datetime.datetime(2022, 1, 1)
    assert deep_equal(d1, d2)
    assert not deep_equal(d1, d3)

def test_handles_complex_nested_structures():
    a = {'arr': [1, {'z': 2}, [3, 4]], 'obj': {'x': 1, 'y': [{'q': 8}]}}
    b = {'arr': [1, {'z': 2}, [3, 4]], 'obj': {'x': 1, 'y': [{'q': 8}]}}
    c = {'arr': [1, {'z': 3}, [3, 4]], 'obj': {'x': 1, 'y': [{'q': 8}]}}
    assert deep_equal(a, b)
    assert not deep_equal(a, c)

def test_handles_arguments_objects():
    def foo(a, b): return (a, b)
    args1 = foo(1, 2)
    args2 = foo(1, 2)
    args3 = foo(2, 3)
    assert deep_equal(args1, args2)
    assert not deep_equal(args1, args3)

def test_different_constructors_with_same_properties():
    class Foo:
        def __init__(self):
            self.x = 5
    class Bar:
        def __init__(self):
            self.x = 5
    assert deep_equal(Foo(), Bar())

def test_buffers():
    a = bytes([1, 2, 3])
    b = bytes([1, 2, 3])
    c = bytes([1, 2, 4])
    assert deep_equal(a, b)
    assert not deep_equal(a, c)

def test_maps_and_sets():
    m1 = {1: 'a', 2: 'b'}
    m2 = {1: 'a', 2: 'b'}
    m3 = {1: 'a', 2: 'c'}
    assert deep_equal(m1, m2)
    assert not deep_equal(m1, m3)

    s1 = set([1, 2, 3])
    s2 = set([1, 2, 3])
    s3 = set([1, 2, 4])
    assert deep_equal(s1, s2)
    assert not deep_equal(s1, s3)

def test_functions_are_only_equal_by_reference():
    def a(): return 1
    def b(): return 1
    assert deep_equal(a, a)
    assert not deep_equal(a, b)