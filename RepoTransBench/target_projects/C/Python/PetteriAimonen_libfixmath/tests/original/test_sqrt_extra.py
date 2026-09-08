from src.libfixmath_python.fix16 import fix16_sqrt

def test_fix16_sqrt_pos():
    assert fix16_sqrt(0) == 0
    assert fix16_sqrt(0x10000) == 0x10000
    assert fix16_sqrt(0x40000) == 0x20000
    assert fix16_sqrt(0x90000) == 0x30000
    assert fix16_sqrt(0x1000000) > 0

def test_fix16_sqrt_neg():
    assert fix16_sqrt(-0x10000) == -0x10000
    assert fix16_sqrt(-0x40000) == -0x20000