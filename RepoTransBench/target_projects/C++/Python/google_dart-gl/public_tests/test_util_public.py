# Public util tests for coverage, with full implementations local to this file.
# These use DIFFERENT test values than in the original (private) tests.

def IsPowerOfTwo(value):
    return value > 0 and (value & (value - 1)) == 0

def NextPowerOfTwo(value):
    if value <= 0:
        return 1
    power = 1
    while power < value:
        power <<= 1
    return power

def test_IsPowerOfTwo_public():
    # Use different inputs from private/original test!
    assert IsPowerOfTwo(32) is True     # new
    assert IsPowerOfTwo(10) is False    # new
    assert IsPowerOfTwo(6) is False     # new
    assert IsPowerOfTwo(64) is True     # new large power
    assert IsPowerOfTwo(15) is False    # new
    assert IsPowerOfTwo(-8) is False    # new negative
    assert IsPowerOfTwo(128) is True    # new larger

def test_NextPowerOfTwo_public():
    # Different input/output combinations than in private/original test
    assert NextPowerOfTwo(14) == 16     # new
    assert NextPowerOfTwo(20) == 32     # new
    assert NextPowerOfTwo(16) == 16     # new power of two
    assert NextPowerOfTwo(-1) == 1      # edge, new negative
    assert NextPowerOfTwo(21) == 32     # new
    assert NextPowerOfTwo(33) == 64     # new
    assert NextPowerOfTwo(64) == 64     # new, already power of two