from src.libfixmath_python.fract32 import fract32_create, fract32_invert, fract32_usmul, fract32_smul

def test_public_test_fract32_create():
    assert fract32_create(30, 10) == 0xFFFFFFFF
    assert fract32_create(255, 255) == 0xFFFFFFFF
    result = fract32_create(7, 13)
    assert result <= 0xFFFFFFFF
    result = fract32_create(50, 51)
    assert result <= 0xFFFFFFFF

def test_public_test_fract32_invert():
    assert fract32_invert(1) == 0xFFFFFFFF - 1
    assert fract32_invert(54321) == 0xFFFFFFFF - 54321
    assert fract32_invert(0xFFFFFFF0) == 0xFFFFFFFF - 0xFFFFFFF0

def test_public_test_fract32_usmul():
    assert fract32_usmul(200, 0x40000000) == 50
    assert fract32_usmul(654321, 0xFFFFFFFF) == 654321
    assert fract32_usmul(6543, 0) == 0

def test_public_test_fract32_smul():
    assert fract32_smul(200, 0x40000000) == 50
    assert fract32_smul(-200, 0x40000000) == -50
    assert fract32_smul(0, 0x40000000) == 0