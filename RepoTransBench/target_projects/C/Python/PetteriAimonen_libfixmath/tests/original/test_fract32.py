from src.libfixmath_python.fract32 import fract32_create, fract32_invert, fract32_usmul, fract32_smul

def test_fract32_create():
    assert fract32_create(10, 5) == 0xFFFFFFFF
    assert fract32_create(100, 100) == 0xFFFFFFFF
    result = fract32_create(5, 10)
    assert result <= 0xFFFFFFFF
    result = fract32_create(9, 10)
    assert result <= 0xFFFFFFFF

def test_fract32_invert():
    assert fract32_invert(0) == 0xFFFFFFFF
    assert fract32_invert(12345) == 0xFFFFFFFF - 12345
    assert fract32_invert(0xFFFFFFFF) == 0

def test_fract32_usmul():
    assert fract32_usmul(100, 0x80000000) == 50
    assert fract32_usmul(123456789, 0xFFFFFFFF) == 123456789
    assert fract32_usmul(12345, 0) == 0

def test_fract32_smul():
    assert fract32_smul(100, 0x80000000) == 50
    assert fract32_smul(-100, 0x80000000) == -50
    assert fract32_smul(0, 0x80000000) == 0