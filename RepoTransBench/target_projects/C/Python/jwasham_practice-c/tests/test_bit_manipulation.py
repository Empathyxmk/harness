import pytest

def btoa(bits, size):
    output = ['0'] * size
    val = bits
    for i in range(size - 1, -1, -1):
        output[i] = str(val & 1)
        val >>= 1
    return ''.join(output)

def is_little_endian():
    import sys
    return sys.byteorder == 'little'

def test_btoa():
    assert btoa(0, 8) == "00000000"
    assert btoa(1, 8) == "00000001"
    assert btoa(0xFF, 8) == "11111111"
    assert btoa(0xAA, 8) == "10101010"

def test_is_little_endian():
    le = is_little_endian()
    assert le in [True, False]

def test_bit_ops():
    x = 0
    x |= (1 << 2)
    assert x == 4

    x &= ~(1 << 2)
    assert x == 0

    x = 65535
    x &= ~(1 << 2)
    assert x == (65535 - 4)