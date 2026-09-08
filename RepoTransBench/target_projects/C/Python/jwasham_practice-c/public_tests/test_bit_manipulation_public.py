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
    # 32-bit for portability (but will work on 64-bit if python is 64bit)
    import sys
    size = 32   # typically sizeof(unsigned int) * 8 in C
    buf = list('?' * (size))
    s = btoa(17, size)
    # 17 is ...000010001
    one_idx1 = size - 5
    one_idx2 = size - 1
    for i in range(size):
        if i == one_idx1 or i == one_idx2:
            assert s[i] == '1'
        else:
            assert s[i] == '0'
    s = btoa(0xFF00, size)
    for i in range(size):
        if i >= size - 16 and i < size - 8:
            assert s[i] == '1'
        else:
            assert s[i] == '0'

def test_is_little_endian():
    value = is_little_endian()
    assert value in [True, False]

def test_bit_ops():
    x = 0
    x |= (1 << 4)
    assert (x & (1 << 4)) != 0

    x = 0xFFFF
    x &= ~(1 << 4)
    assert (x & (1 << 4)) == 0

    x = 0
    b = (32 - 2)
    x |= (1 << b)
    assert (x & (1 << b)) != 0