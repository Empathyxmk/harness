import pytest

UTF8_MAXCP = 0x10FFFF

def utf8_invalid(ch):
    return (ch > UTF8_MAXCP or (0xD800 <= ch <= 0xDFFF))

def utf8_encode(x):
    buff = [0] * 8
    n = 1
    tmp = x
    if x < 0x80:
        buff[-1] = x & 0x7F
    else:
        n = 1
        mfb = 0x3f
        sz = 8
        while True:
            buff[sz-n] = 0x80 | (x & 0x3f)
            x >>= 6
            mfb >>= 1
            n += 1
            if x <= mfb:
                break
        buff[sz-n] = ((~mfb << 1) | x) & 0xFF
    return buff, n

def test_utf8_invalid():
    assert utf8_invalid(0x10FFFF) == False
    assert utf8_invalid(0x110000) == True
    assert utf8_invalid(0xD800) == True
    assert utf8_invalid(0xDFFF) == True
    assert utf8_invalid(0x7FFF) == False

def test_utf8_encode_ascii():
    buff, n = utf8_encode(0x41)  # 'A'
    assert n == 1
    assert buff[-1] == 0x41

def test_utf8_encode_multibyte():
    buff, n = utf8_encode(0x20AC)  # €
    assert n > 1
    assert buff[-1] == 0xAC

def test_utf8_encode_fourbyte():
    buff, n = utf8_encode(0x1F600)  # 😀
    assert 1 <= n <= 4
    # Not testing value, ensuring no crash