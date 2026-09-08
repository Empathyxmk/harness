import pytest
import re
import math

from src.fast_deep_equal.index import fast_deep_equal as equal

def test_equal_primitives_public():
    assert equal(42, 42) is True
    assert equal("public", "public") is True
    assert equal(None, None) is True
    assert equal(None, None) is True
    assert equal(False, False) is True
    assert equal(True, True) is True

def test_different_primitives_public():
    assert equal(99, 100) is False
    assert equal("alpha", "beta") is False
    assert equal(None, False) is False
    assert equal(False, True) is False

def test_objects_equal_and_not_equal_public():
    assert equal({"x": 9}, {"x": 9}) is True
    assert equal({"x": 9}, {"x": 10}) is False
    assert equal({"a": 2}, {"b": 2}) is False
    assert equal({"first": 1, "second": 2}, {"second": 2, "first": 1}) is True
    assert equal({"tag": "open"}, {"tag": "open"}) is True
    assert equal({}, {}) is True

def test_arrays_equal_and_not_equal_public():
    assert equal([10, 20, 30], [10, 20, 30]) is True
    assert equal([10, 20, 30], [10, 20]) is False
    assert equal([5, 6, 7], [7, 6, 5]) is False
    assert equal([], []) is True

def test_nested_structures_public():
    assert equal({"x": [5, 6, {"y": 7}]}, {"x": [5, 6, {"y": 7}]}) is True
    assert equal({"x": [5, 6, {"y": 7}]}, {"x": [5, 6, {"y": 8}]}) is False

def test_regexp_public():
    # Use valid Python regex flags
    assert equal(re.compile("b", re.I), re.compile("b", re.I)) is True
    assert equal(re.compile("b", re.I), re.compile("b", re.M)) is False
    assert equal(re.compile("b"), re.compile("c")) is False

def test_different_constructors_public():
    import datetime
    assert equal({}, datetime.datetime.now()) is False

    class FooBar:
        def __init__(self): self.y = 5

    class Baz:
        def __init__(self): self.y = 5

    fooBar = FooBar()
    baz = Baz()
    assert equal(fooBar, baz) is False

def test_valueof_property_public():
    class Val:
        def __init__(self, u): self.u = u
        def valueOf(self): return self.u
    d = Val(99)
    e = Val(99)
    f = Val(100)
    assert equal(d, e) is True
    assert equal(d, f) is False

    class Dummy:
        def valueOf(self): return 10
    o1 = Dummy()
    o2 = Dummy()
    assert equal(o1, o2) is True
    class Dummy2:
        def valueOf(self): return 11
    o3 = Dummy2()
    assert equal(o1, o3) is False

def test_tostring_property_public():
    class WithToString:
        def __init__(self, val): self.val = val
        def toString(self): return self.val
    a = WithToString("baz")
    b = WithToString("baz")
    c = WithToString("qux")
    assert equal(a, b) is True
    assert equal(a, c) is False

def test_objects_with_missing_keys_public():
    assert equal({"x": 5, "y": 8}, {"x": 5}) is False
    assert equal({"x": 5}, {"x": 5, "y": 8}) is False

def test_objects_with_extra_keys_public():
    assert equal({"x": 7, "y": None}, {"x": 7}) is False

def test_hasownproperty_edge_case_public():
    class A:
        pass
    a = A()
    b = A()
    a.k = 14
    b.k = 14
    import types
    def vfunc(self): return "[x]"
    a.valueOf = types.MethodType(vfunc, a)
    b.valueOf = types.MethodType(vfunc, b)
    assert equal(a, b) is True
    b.z = 9
    def vfuncb(self): return "[y]"
    b.valueOf = types.MethodType(vfuncb, b)
    assert equal(a, b) is False

def test_nan_public():
    assert equal(math.nan, math.nan) is True
    assert equal(math.nan, 99) is False
    assert equal(99, math.nan) is False

def test_non_object_primitive_public():
    assert equal(100, {"value": 100}) is False
    assert equal([3, 4], {0: 3, 1: 4}) is False

def test_deeply_nested_public():
    obj1 = {"p": {"q": {"r": [8, 9, "x"], "s": "t"}}}
    obj2 = {"p": {"q": {"r": [8, 9, "x"], "s": "t"}}}
    obj3 = {"p": {"q": {"r": [8, 9, "y"], "s": "t"}}}
    assert equal(obj1, obj2) is True
    assert equal(obj1, obj3) is False

def test_no_throw_on_missing_valueof_tostring_public():
    class Blank:
        pass
    a = Blank()
    b = Blank()
    a.alpha = 456
    b.alpha = 456
    a.valueOf = object.__str__
    b.valueOf = object.__str__
    a.toString = object.__str__
    b.toString = object.__str__
    assert equal(a, b) is True