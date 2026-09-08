# Original util tests for coverage.
# The implementations are made local to this file, following the C++ logic.

def IsPowerOfTwo(value):
    return value > 0 and (value & (value - 1)) == 0

def NextPowerOfTwo(value):
    if value <= 0:
        return 1
    power = 1
    while power < value:
        power <<= 1
    return power

def test_IsPowerOfTwo():
    assert IsPowerOfTwo(1) is True
    assert IsPowerOfTwo(2) is True
    assert IsPowerOfTwo(3) is False
    assert IsPowerOfTwo(4) is True
    assert IsPowerOfTwo(0) is False
    assert IsPowerOfTwo(16) is True
    assert IsPowerOfTwo(18) is False

def test_NextPowerOfTwo():
    assert NextPowerOfTwo(0) == 1
    assert NextPowerOfTwo(1) == 1
    assert NextPowerOfTwo(2) == 2
    assert NextPowerOfTwo(3) == 4
    assert NextPowerOfTwo(5) == 8
    assert NextPowerOfTwo(7) == 8
    assert NextPowerOfTwo(8) == 8
    assert NextPowerOfTwo(9) == 16
    assert NextPowerOfTwo(-3) == 1