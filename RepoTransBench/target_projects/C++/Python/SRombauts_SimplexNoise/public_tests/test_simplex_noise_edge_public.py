import math
import pytest

from src.simplex_noise.simplex_noise import SimplexNoise

def nearly_equal(a, b, epsilon=1e-5):
    return abs(a - b) < epsilon

def test_edge_float_values_public():
    # Instead of 0.0, 10000, -10000 use different values
    val1 = SimplexNoise.noise(123.456)
    val2 = SimplexNoise.noise(-987.654)
    val3 = SimplexNoise.noise(9999.99)
    # Just check the values for expected constraints
    assert -1.0 <= val1 <= 1.0
    assert -1.0 <= val2 <= 1.0
    assert -1.0 <= val3 <= 1.0

def test_edge_2d_input_public():
    # Use different 2D values than private tests
    v1 = SimplexNoise.noise(123.45, -321.54)
    v2 = SimplexNoise.noise(-456.789, 789.456)
    assert -1.0 <= v1 <= 1.0
    assert -1.0 <= v2 <= 1.0

def test_repeatability_public():
    # Confirm deterministic property for new values
    a = SimplexNoise.noise(567.89, 321.123)
    b = SimplexNoise.noise(567.89, 321.123)
    assert nearly_equal(a, b)

def test_edge_cases_3d_public():
    val1 = SimplexNoise.noise(9.876, -5.432, 1.234)
    val2 = SimplexNoise.noise(999.99, -999.99, 0.0)
    assert -1.0 <= val1 <= 1.0
    assert -1.0 <= val2 <= 1.0

def test_repeatability_3d_public():
    v1a = SimplexNoise.noise(-321.123, 654.456, 987.789)
    v1b = SimplexNoise.noise(-321.123, 654.456, 987.789)
    assert nearly_equal(v1a, v1b)