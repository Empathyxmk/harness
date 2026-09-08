import pytest
from src.utf8.utf8 import utf8_decode

def test_ascii():
    buf = [ord('A'), 0, 0, 0]
    val, length, err = utf8_decode(buf[:1])
    assert length == 1
    assert err == 0
    assert val == ord('A')

def test_2byte():
    buf = [0xC2, 0xA2, 0, 0] # U+00A2: ¢
    val, length, err = utf8_decode(buf[:2])
    assert length == 2
    assert err == 0
    assert val == 0xA2

def test_3byte():
    buf = [0xE2, 0x82, 0xAC, 0] # U+20AC: €
    val, length, err = utf8_decode(buf[:3])
    assert length == 3
    assert err == 0
    assert val == 0x20AC

def test_4byte():
    buf = [0xF0, 0x9F, 0x98, 0x81] # U+1F601: 😁
    val, length, err = utf8_decode(buf[:4])
    assert length == 4
    assert err == 0
    assert val == 0x1F601

def test_invalid_1():
    buf = [0xFF, 0, 0, 0]
    val, length, err = utf8_decode(buf[:1])
    assert err != 0

def test_truncated():
    buf = [0xE2, 0x28, 0, 0]
    val, length, err = utf8_decode(buf[:2])
    assert err != 0

def test_surrogate():
    buf = [0xED, 0xA0, 0x80, 0]
    val, length, err = utf8_decode(buf[:3])
    assert err != 0

def run_all():
    test_ascii()
    test_2byte()
    test_3byte()
    test_4byte()
    test_invalid_1()
    test_truncated()
    test_surrogate()

if __name__ == "__main__":
    run_all()
    print("All utf8_decode tests passed")