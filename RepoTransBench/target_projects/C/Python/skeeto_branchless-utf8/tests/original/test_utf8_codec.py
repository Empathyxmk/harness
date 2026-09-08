import pytest
from src.utf8.utf8 import utf8_encode, utf8_decode, is_surrogate

def test_decode_all():
    failures = 0
    for i in range(0x110000):
        if not is_surrogate(i):
            buf = []
            n = utf8_encode(buf, i)
            if n == 0:
                continue
            val, length, err = utf8_decode(buf)
            if length != n or val != i or err:
                failures += 1
    assert failures == 0, f"decode all, errors: {failures}"

def test_out_of_range():
    failures = 0
    for i in range(0x110000, 0x1FFFFF):
        buf = []
        utf8_encode(buf, i)
        val, length, err = utf8_decode(buf)
        # Should error out
        if err == 0:
            failures += 1
        if length and length != 4:
            failures += 1
    assert failures == 0, f"out of range, errors: {failures}"

def test_surrogate_halves():
    failures = 0
    for i in range(0xD800, 0xE000):
        buf = []
        utf8_encode(buf, i)
        val, length, err = utf8_decode(buf)
        if err == 0:
            failures += 1
    assert failures == 0, f"surrogate halves, errors: {failures}"

def test_noncanonical_encodings():
    # Overlong encodings and invalid forms
    e, c = None, None
    buf2 = [0xC0, 0xA4] # 2-byte overlong
    val, length, err = utf8_decode(buf2)
    assert err and length == 2, f"non-canonical len 2, {err}"
    buf3 = [0xE0, 0x80, 0xA4]
    val, length, err = utf8_decode(buf3)
    assert err and length == 3, f"non-canonical len 3, {err}"
    buf4 = [0xF0, 0x80, 0x80, 0xA4]
    val, length, err = utf8_decode(buf4)
    assert err and length == 4, f"non-canonical len 4, {err}"

def test_bogus_bytes():
    # Various invalid sequences
    buf0 = [0xFF]
    val, length, err = utf8_decode(buf0)
    assert err and length == 1
    buf1 = [0x80]
    val, length, err = utf8_decode(buf1)
    assert err and length == 1
    buf2 = [0xC0, 0x0A]
    val, length, err = utf8_decode(buf2)
    assert err and length == 2