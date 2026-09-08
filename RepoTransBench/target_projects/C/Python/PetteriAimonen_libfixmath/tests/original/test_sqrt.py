from src.libfixmath_python.fix16 import fix16_from_int, fix16_sqrt, fix16_to_dbl
import math
from src.libfixmath_python.testcases import testcases

def test_sqrt_specific():
    assert fix16_sqrt(fix16_from_int(16)) == fix16_from_int(4)
    assert fix16_sqrt(fix16_from_int(100)) == fix16_from_int(10)
    assert fix16_sqrt(fix16_from_int(1)) == fix16_from_int(1)
    assert fix16_sqrt(214748302) == 3751499
    assert fix16_sqrt(214748303) == 3751499
    assert fix16_sqrt(214748359) == 3751499
    assert fix16_sqrt(214748360) == 3751500

def test_sqrt_short():
    for a in testcases:
        fa = fix16_to_dbl(a)
        result = fix16_sqrt(a)
        fresult = math.sqrt(fa)
        assert math.isclose(fix16_to_dbl(result), fresult, abs_tol=1), f"in: {fa}"