import pytest
from src.utf8.utf8 import utf8_decode

def test_one_byte():
    b1 = [0x7A, 0x00]
    val, length, err = utf8_decode(b1[:1])
    assert val == 0x7A and not err

def test_two_byte():
    b2 = [0xC2, 0xA9, 0x00]
    val, length, err = utf8_decode(b2[:2])
    assert val == 0xA9 and not err

def test_three_byte():
    b3 = [0xE2, 0x82, 0xAC, 0x00]
    val, length, err = utf8_decode(b3[:3])
    assert val == 0x20AC and not err

def test_four_byte():
    b4 = [0xF0, 0x9F, 0x9A, 0x80, 0x00]
    val, length, err = utf8_decode(b4[:4])
    assert val == 0x1F680 and not err

def test_overlong_2byte():
    overlong2 = [0xC0, 0x80, 0x00]
    val, length, err = utf8_decode(overlong2[:2])
    assert err

def test_overlong_3byte():
    overlong3 = [0xE0, 0x80, 0x80, 0x00]
    val, length, err = utf8_decode(overlong3[:3])
    assert err

def test_invalid_first_byte():
    inv1 = [0xFF, 0x00]
    val, length, err = utf8_decode(inv1[:1])
    assert err

def test_valid_2byte():
    max2 = [0xDF, 0xBF, 0x00]
    val, length, err = utf8_decode(max2[:2])
    assert val == 0x7FF and not err

def test_valid_3byte():
    max3 = [0xEF, 0xBF, 0xBF, 0x00]
    val, length, err = utf8_decode(max3[:3])
    assert val == 0xFFFF and not err

def test_out_of_range():
    oor = [0xF4, 0x90, 0x80, 0x80, 0x00]
    val, length, err = utf8_decode(oor[:4])
    assert err

def test_surrogate():
    surrogate = [0xED, 0xBF, 0xBF, 0x00]
    val, length, err = utf8_decode(surrogate[:3])
    assert err