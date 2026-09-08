import pytest
from protofuzz import values

def test_integral_value_gen_public():
    g = values.integral_value_gen()
    # The generator has a finite number of values; exhaust it and check.
    vals = list(g)
    assert all(isinstance(v, int) for v in vals)
    assert len(set(vals)) == len(vals)
    # Additional check: list is not empty and covers both pos/neg integers
    assert any(v < 0 for v in vals) and any(v >= 0 for v in vals)
    assert len(vals) > 5

def test_float32_value_gen_public():
    g = values.float32_value_gen()
    vals = list(g)
    assert all(isinstance(v, float) for v in vals)
    assert len(set(vals)) == len(vals)
    assert any(abs(v) < 1.0 for v in vals)
    assert any(abs(v) > 1.0 for v in vals)
    assert len(vals) > 7

def test_string_value_gen_public():
    g = values.string_value_gen()
    vals = list(g)
    # Original test may have checked length; here, we assert various string properties
    assert all(isinstance(v, str) for v in vals)
    assert len(set(vals)) == len(vals)
    # Ensure at least some strings have visible characters, and some could be empty or special
    assert any(len(v) > 3 for v in vals)
    assert len(vals) > 5