import pytest
import re
import math

from src.fast_deep_equal.index import fast_deep_equal as equal

def test_equal_primitives():
    assert equal(1, 1) is True
    assert equal("a", "a") is True
    assert equal(None, None) is True
    assert equal(None, None) is True
    assert equal(True, True) is True
    assert equal(False, False) is True

def test_different_primitives():
    assert equal(1, 2) is False
    assert equal("a", "b") is False
    # The JS test has null vs undefined; here None vs None, keep True
    assert equal(None, None) is True
    assert equal(True, False) is False

def test_objects_equal_and_not_equal():
    assert equal({"a": 1}, {"a": 1}) is True
    assert equal({"a": 1}, {"a": 2}) is False
    assert equal({"a": 1}, {"b": 1}) is False
    assert equal({"a": 1, "b": 2}, {"b": 2, "a": 1}) is True
    assert equal({}, {}) is True

def test_arrays_equal_and_not_equal():
    assert equal([1, 2, 3], [1, 2, 3]) is True
    assert equal([1, 2, 3], [1, 2]) is False
    assert equal([1, 2, 3], [3, 2, 1]) is False
    assert equal([], []) is True

def test_nested_structures():
    assert equal({"a": [1, 2, {"b": 3}]}, {"a": [1, 2, {"b": 3}]}) is True
    assert equal({"a": [1, 2, {"b": 3}]}, {"a": [1, 2, {"b": 4}]}) is False

def test_regexp():
    # Use different valid re flags (gloabl flag does not exist in Python)
    assert equal(re.compile("a", re.I), re.compile("a", re.I)) is True
    assert equal(re.compile("a", re.I), re.compile("a", re.M)) is False
    assert equal(re.compile("a"), re.compile("b")) is False

def test_different_constructors():
    assert equal({}, []) is False

    class Foo:
        def __init__(self):
            self.x = 1

    class Bar:
        def __init__(self):
            self.x = 1

    foo = Foo()
    bar = Bar()
    assert equal(foo, bar) is False

def test_valueof_property():
    class V:
        def __init__(self, v):
            self.v = v
        def valueOf(self):
            return self.v
    a = V(42)
    b = V(42)
    c = V(43)
    assert equal(a, b) is True
    assert equal(a, c) is False

    # Ensure both objects use valueOf for comparison
    class Dummy:
        def valueOf(self): return 5
    o1 = Dummy()
    o2 = Dummy()
    assert equal(o1, o2) is True
    class Dummy2:
        def valueOf(self): return 6
    o3 = Dummy2()
    assert equal(o1, o3) is False

def test_tostring_property():
    class WithToString:
        def __init__(self, val):
            self.val = val
        def toString(self):
            return self.val
    a = WithToString("foo")
    b = WithToString("foo")
    c = WithToString("bar")
    assert equal(a, b) is True
    assert equal(a, c) is False

def test_objects_with_missing_keys():
    assert equal({"a": 1, "b": 2}, {"a": 1}) is False
    assert equal({"a": 1}, {"a": 1, "b": 2}) is False

def test_objects_with_extra_keys():
    assert equal({"a": 1, "b": None}, {"a": 1}) is False

def test_hasownproperty_edge_case():
    # In Python, objects with no __dict__ can be created using type()
    class A:
        pass
    a = A()
    b = A()
    a.x = 1
    b.x = 1
    # add valueOf method
    import types
    def vfunc(self): return "[a]"
    a.valueOf = types.MethodType(vfunc, a)
    b.valueOf = types.MethodType(vfunc, b)
    assert equal(a, b) is True
    b.y = 2
    def vfuncb(self): return "[b]"
    b.valueOf = types.MethodType(vfuncb, b)
    assert equal(a, b) is False

def test_nan():
    assert equal(math.nan, math.nan) is True
    assert equal(math.nan, 1) is False
    assert equal(1, math.nan) is False

def test_non_object_primitive():
    assert equal(3, {"a": 3}) is False
    assert equal([1, 2], {0: 1, 1: 2}) is False

def test_deeply_nested():
    obj1 = {"a": {"b": {"c": [1, 2, 3], "d": "e"}}}
    obj2 = {"a": {"b": {"c": [1, 2, 3], "d": "e"}}}
    obj3 = {"a": {"b": {"c": [1, 2, 4], "d": "e"}}}
    assert equal(obj1, obj2) is True
    assert equal(obj1, obj3) is False

def test_no_throw_on_missing_valueof_tostring():
    class Blank:
        pass
    a = Blank()
    b = Blank()
    a.test = 123
    b.test = 123
    # Add valueOf and toString as attributes (can use object.__str__)
    a.valueOf = object.__str__
    b.valueOf = object.__str__
    a.toString = object.__str__
    b.toString = object.__str__
    assert equal(a, b) is True