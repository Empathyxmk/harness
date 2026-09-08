import pytest
from src.is_number import is_number

def test_non_string_non_number_object():
    assert is_number({'a': 1}) is False

def test_undefined_none():
    assert is_number(None) is False

def test_null_none():
    assert is_number(None) is False

def test_array():
    assert is_number([1, 2]) is False

def test_empty_string():
    assert is_number('') is False

def test_whitespace_string():
    assert is_number('   ') is False

def test_string_non_numeric():
    assert is_number('foo') is False

def test_nan():
    import math
    assert is_number(float('nan')) is False

def test_number_isfinite_polyfill(monkeypatch):
    # Simulate the absence of isfinite by monkeypatching math.isfinite
    import math
    orig = math.isfinite
    monkeypatch.setattr(math, "isfinite", None)
    assert is_number('123') is True
    monkeypatch.setattr(math, "isfinite", orig)

def test_leading_trailing_whitespace():
    assert is_number(' 42 ') is True