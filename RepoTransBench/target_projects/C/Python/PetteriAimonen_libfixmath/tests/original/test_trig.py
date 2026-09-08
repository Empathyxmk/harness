from src.libfixmath_python.fix16_trig import fix16_sin_parabola, fix16_sin
from src.libfixmath_python.fix16 import fix16_pi

def test_fix16_sin_parabola():
    assert fix16_sin_parabola(0) < 100
    assert fix16_sin_parabola(fix16_pi // 2) > 0
    assert fix16_sin_parabola(-fix16_pi // 2) < 0

def test_fix16_sin():
    assert fix16_sin(0) < 100
    assert fix16_sin(fix16_pi) < 100
    assert fix16_sin(fix16_pi // 2) > 0
    assert fix16_sin(-fix16_pi // 2) < 0
    assert fix16_sin(10 * fix16_pi) < 100