import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from paramparser import ParamSpec

def test_ParamSpec_basic():
    p = ParamSpec("anotherparam", "anotherval")
    assert hasattr(p, "paramName")

def test_ParamSpec_str():
    # different test data
    p = ParamSpec("customparam", "val42")
    assert str(p) == "(customparam, val42)"

def test_ParamSpec_eq():
    p1 = ParamSpec("eqtest", "a")
    p2 = ParamSpec("eqtest", "a")
    p3 = ParamSpec("eqtest", "b")
    assert p1 == p2
    assert p1 != p3