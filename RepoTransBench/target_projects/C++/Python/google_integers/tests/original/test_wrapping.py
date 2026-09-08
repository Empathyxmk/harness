import pytest

def wrap_int(value, modulo):
    rem = value % modulo
    return rem if rem >= 0 else rem + modulo

def test_simple_wrap():
    maxnum = 255
    input_value = 257
    wrapped = wrap_int(input_value, maxnum + 1)
    assert wrapped == 1  # 257 % 256 == 1

def test_negative_wrap():
    maxnum = 255
    input_value = -2
    wrapped = wrap_int(input_value, maxnum + 1)
    assert wrapped == 254  # -2 wraps to 254

def test_no_wrap():
    maxnum = 255
    input_value = 100
    wrapped = wrap_int(input_value, maxnum + 1)
    assert wrapped == 100  # No wrap