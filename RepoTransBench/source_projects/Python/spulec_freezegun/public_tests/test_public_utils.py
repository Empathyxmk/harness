import math

def test_public_utils_isclose():
    # Use different numbers than any original
    assert math.isclose(13.000001, 13.000002, rel_tol=1e-5)

def test_public_utils_trunc():
    assert math.trunc(152.67) == 152

def test_public_utils_factorial():
    assert math.factorial(6) == 720