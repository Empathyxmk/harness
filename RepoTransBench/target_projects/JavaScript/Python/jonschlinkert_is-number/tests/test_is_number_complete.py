import pytest
from src.is_number import is_number

def test_integer_strings():
    assert is_number('123') is True
    assert is_number('-123') is True
    assert is_number('+123') is True

def test_normal_numbers():
    assert is_number(123) is True
    assert is_number(-123) is True
    assert is_number(0) is True

def test_numeric_but_not_finite():
    import math
    assert is_number(float("inf")) is False
    assert is_number(float("-inf")) is False
    assert is_number(float("nan")) is False
    assert is_number('NaN') is False

def test_floats():
    assert is_number(3.14) is True
    assert is_number('3.14') is True

def test_scientific_notation():
    assert is_number('1e3') is True
    assert is_number('-1e-3') is True
    assert is_number('0.1e+2') is True

def test_strings_with_spaces_mid_value():
    assert is_number('1 2 3') is False
    assert is_number('1 2') is False
    assert is_number('1. 0') is False

def test_non_numeric_strings():
    assert is_number('abc') is False
    assert is_number('123abc') is False
    assert is_number('abc123') is False
    assert is_number('++123') is False
    assert is_number('--123') is False
    assert is_number(' 123abc') is False
    assert is_number('abc123 ') is False

def test_objects_arrays_null_undefined():
    assert is_number([]) is False
    assert is_number({}) is False
    assert is_number(None) is False
    assert is_number(None) is False
    import datetime
    assert is_number(datetime.datetime.now()) is False

def test_boolean_values():
    assert is_number(True) is False
    assert is_number(False) is False

def test_empty_and_whitespace_strings():
    assert is_number('') is False
    assert is_number('   ') is False
    assert is_number('\n\t') is False

def test_number_objects():
    # Python does not wrap numbers like JS Object(1), but we simulate with objects
    # There is no direct equivalent, but any object is not a number
    class NumberLike:
        def __init__(self, value): self.value = value
    assert is_number(NumberLike(1)) is False
    assert is_number(NumberLike(3.14)) is False
    assert is_number(NumberLike('1')) is False

def test_functions():
    assert is_number(lambda: None) is False
    def f(): return 1
    assert is_number(f) is False

def test_hex_bin_oct_numeric_strings():
    assert is_number('0x11') is True
    assert is_number('0b11') is True
    assert is_number('0o11') is True
    assert is_number('0xGHI') is False

def test_isfinite_polyfill(monkeypatch):
    import math
    orig = math.isfinite if hasattr(math, "isfinite") else None
    if hasattr(math, "isfinite"):
        monkeypatch.delattr(math, "isfinite")
    assert is_number(45) is True
    if orig is not None:
        monkeypatch.setattr(math, "isfinite", orig)