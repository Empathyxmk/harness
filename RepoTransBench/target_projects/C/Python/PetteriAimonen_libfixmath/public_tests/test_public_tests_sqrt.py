import math
import pytest
from src.libfixmath_python.fix16 import fix16_from_int, fix16_sqrt, fix16_to_dbl

def test_public_test_sqrt_specific():
    assert fix16_sqrt(fix16_from_int(25)) == fix16_from_int(5)
    assert fix16_sqrt(fix16_from_int(4)) == fix16_from_int(2)
    assert fix16_sqrt(fix16_from_int(49)) == fix16_from_int(7)
    assert fix16_sqrt(314159265) == 56051
    assert fix16_sqrt(314159266) == 56051
    assert fix16_sqrt(314159299) == 56051
    assert fix16_sqrt(314159300) == 56052

def test_public_test_sqrt_short():
    testcases = [
        fix16_from_int(2),
        fix16_from_int(81),
        fix16_from_int(0),
        fix16_from_int(12345),
        fix16_from_int(225)
    ]
    for a in testcases:
        fa = fix16_to_dbl(a)
        result = fix16_sqrt(a)
        fresult = math.sqrt(fa)
        assert math.isclose(fix16_to_dbl(result), fresult, abs_tol=1)