import pytest

def wrap_int(value, modulo):
    rem = value % modulo
    return rem if rem >= 0 else rem + modulo

def test_wrap_public():
    assert wrap_int(14, 5) == 4    # 14 mod 5 = 4
    assert wrap_int(-7, 5) == 3    # -7 mod 5 = 3
    assert wrap_int(0, 7) == 0     # 0 mod 7 = 0
    assert wrap_int(21, 7) == 0    # 21 mod 7 = 0
    assert wrap_int(-15, 4) == 1   # -15 mod 4 = 1