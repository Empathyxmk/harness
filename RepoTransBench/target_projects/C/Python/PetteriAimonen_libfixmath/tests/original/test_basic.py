import math
import pytest
from src.libfixmath_python.fix16 import (
    fix16_from_int, fix16_to_dbl, fix16_abs, fix16_add, fix16_mul, fix16_div, fix16_sub,
    fix16_maximum, fix16_minimum, fix16_overflow, fix16_eps,
)
from src.libfixmath_python.testcases import testcases, TESTCASES_COUNT

@pytest.mark.parametrize("a", testcases)
def test_abs_short(a):
    fa = fix16_to_dbl(a)
    result = fix16_abs(a)
    fresult = abs(fa)
    minval = fix16_to_dbl(fix16_minimum)
    if fa <= minval:
        # Overflow in abs
        assert result == fix16_overflow
    else:
        assert math.isclose(fix16_to_dbl(result), fresult, abs_tol=fix16_to_dbl(fix16_eps)), f"in: {fa}"

@pytest.mark.parametrize("a", [None])
def test_abs(a):
    test_abs_short(testcases[0])  # Just ensure one call, pytest will find parametrized

@pytest.mark.parametrize("a", testcases)
@pytest.mark.parametrize("b", testcases)
def test_add_short(a, b):
    result = fix16_add(a, b)
    fa = fix16_to_dbl(a)
    fb = fix16_to_dbl(b)
    fresult = fa + fb
    maxv = fix16_to_dbl(fix16_maximum)
    minv = fix16_to_dbl(fix16_minimum)
    if (fa + fb > maxv) or (fa + fb < minv):
        assert result == fix16_overflow
    else:
        assert math.isclose(fix16_to_dbl(result), fresult, abs_tol=fix16_to_dbl(fix16_eps)), f"{fa} + {fb}"

@pytest.mark.parametrize("a", [None])
def test_add(a):
    # Just to match C structure
    test_add_short(testcases[0], testcases[0])

def test_mul_specific():
    assert fix16_mul(fix16_from_int(5), fix16_from_int(5)) == fix16_from_int(25)
    assert fix16_mul(fix16_from_int(-5), fix16_from_int(5)) == fix16_from_int(-25)
    assert fix16_mul(fix16_from_int(-5), fix16_from_int(-5)) == fix16_from_int(25)
    assert fix16_mul(fix16_from_int(5), fix16_from_int(-5)) == fix16_from_int(-25)

    assert fix16_mul(0, 10) == 0
    assert fix16_mul(2, 0x8000) == 1
    assert fix16_mul(-2, 0x8000) == -1
    assert fix16_mul(3, 0x8000) == 2
    assert fix16_mul(2, 0x7FFF) == 1
    assert fix16_mul(-2, 0x8001) == -1
    assert fix16_mul(-3, 0x8000) == -2
    assert fix16_mul(-2, 0x7FFF) == -1
    assert fix16_mul(2, 0x8001) == 1

@pytest.mark.parametrize("a", testcases)
@pytest.mark.parametrize("b", testcases)
def test_mul_short(a, b):
    result = fix16_mul(a, b)
    fa = fix16_to_dbl(a)
    fb = fix16_to_dbl(b)
    fresult = fa * fb
    maxv = fix16_to_dbl(fix16_maximum)
    minv = fix16_to_dbl(fix16_minimum)
    if fa * fb > maxv or fa * fb < minv:
        assert result == fix16_overflow
    else:
        assert math.isclose(fix16_to_dbl(result), fresult, abs_tol=fix16_to_dbl(fix16_eps)), f"{fa} * {fb}"

@pytest.mark.parametrize("a", [None])
def test_mul(a):
    test_mul_specific()

def test_div_specific():
    assert fix16_div(fix16_from_int(15), fix16_from_int(5)) == fix16_from_int(3)
    assert fix16_div(fix16_from_int(-15), fix16_from_int(5)) == fix16_from_int(-3)
    assert fix16_div(fix16_from_int(-15), fix16_from_int(-5)) == fix16_from_int(3)
    assert fix16_div(fix16_from_int(15), fix16_from_int(-5)) == fix16_from_int(-3)
    assert fix16_div(0, 10) == 0
    assert fix16_div(1, fix16_from_int(2)) == 1
    assert fix16_div(-1, fix16_from_int(2)) == -1
    assert fix16_div(1, fix16_from_int(-2)) == -1
    assert fix16_div(-1, fix16_from_int(-2)) == 1
    assert fix16_div(3, fix16_from_int(2)) == 2
    assert fix16_div(-3, fix16_from_int(2)) == -2
    assert fix16_div(3, fix16_from_int(-2)) == -2
    assert fix16_div(-3, fix16_from_int(-2)) == 2
    assert fix16_div(2, 0x7FFF) == 4
    assert fix16_div(-2, 0x7FFF) == -4
    assert fix16_div(2, 0x8001) == 4
    assert fix16_div(-2, 0x8001) == -4

@pytest.mark.parametrize("a", testcases)
@pytest.mark.parametrize("b", testcases)
def test_div_short(a, b):
    if b == 0:
        return
    result = fix16_div(a, b)
    fa = fix16_to_dbl(a)
    fb = fix16_to_dbl(b)
    fresult = fa / fb
    maxv = fix16_to_dbl(fix16_maximum)
    minv = fix16_to_dbl(fix16_minimum)
    if (fa / fb) > maxv or (fa / fb) < minv:
        assert result == fix16_overflow
    else:
        assert math.isclose(fix16_to_dbl(result), fresult, abs_tol=fix16_to_dbl(fix16_eps)), f"{a} / {b}"

@pytest.mark.parametrize("a", [None])
def test_div(a):
    test_div_specific()

@pytest.mark.parametrize("a", testcases)
@pytest.mark.parametrize("b", testcases)
def test_sub_short(a, b):
    result = fix16_sub(a, b)
    fa = fix16_to_dbl(a)
    fb = fix16_to_dbl(b)
    fresult = fa - fb
    maxv = fix16_to_dbl(fix16_maximum)
    minv = fix16_to_dbl(fix16_minimum)
    if (fa - fb > maxv) or (fa - fb < minv):
        assert result == fix16_overflow
    else:
        assert math.isclose(fix16_to_dbl(result), fresult, abs_tol=fix16_to_dbl(fix16_eps)), f"{fa} - {fb}"

@pytest.mark.parametrize("a", [None])
def test_sub(a):
    test_sub_short(testcases[0], testcases[0])