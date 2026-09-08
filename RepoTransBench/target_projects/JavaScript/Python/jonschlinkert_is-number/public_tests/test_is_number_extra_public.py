import pytest
from src.is_number import is_number

def test_symbol_is_not_number():
    # Python has no Symbol, but we simulate with a unique object
    class Symbol: pass
    assert is_number(Symbol()) is False

def test_function_is_not_number():
    def f(): pass
    assert is_number(f) is False

def test_boolean_true_is_not_number():
    assert is_number(True) is False

def test_array_three_elements_is_not_number():
    assert is_number([7, 8, 9]) is False

def test_string_tabs_only():
    assert is_number('\t\t\t') is False

def test_string_newline_spaces():
    assert is_number('\n   ') is False

def test_string_alphanumeric():
    assert is_number('123abc') is False

def test_negative_nan():
    import math
    assert is_number(-float('nan')) is False

def test_number_isfinite_polyfill_negative(monkeypatch):
    # Simulate missing math.isfinite
    import math
    orig = math.isfinite if hasattr(math, "isfinite") else None
    if hasattr(math, "isfinite"):
        monkeypatch.delattr(math, "isfinite")
    assert is_number('-321') is True
    if orig is not None:
        monkeypatch.setattr(math, "isfinite", orig)

def test_string_with_numbers_inside_newline():
    assert is_number('\n58\n') is True