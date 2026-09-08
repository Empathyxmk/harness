import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from paramparser import ParamSpec

def test_ParamSpec_name_value():
    spec = ParamSpec("public_name", "17")
    assert spec.paramName == "public_name"
    assert spec.paramValue == "17"

def test_ParamSpec_str_and_eq():
    spec1 = ParamSpec("ab", "9")
    spec2 = ParamSpec("ab", "9")
    spec3 = ParamSpec("ab", "8")
    assert str(spec1) == "(ab, 9)"
    assert spec1 == spec2
    assert spec1 != spec3