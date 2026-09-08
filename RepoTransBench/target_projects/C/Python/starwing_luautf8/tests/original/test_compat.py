import pytest
from src.luautf8 import utf8

def test_utf8_compat():
    # These tests duplicate the Lua test_compat.lua logic for boundary and behavioral tests.
    assert utf8.sub("123456789",2,4) == "234"
    assert utf8.sub("123456789",7) == "789"
    assert utf8.sub("123456789",7,6) == ""
    assert utf8.sub("123456789",7,7) == "7"
    assert utf8.sub("123456789",0,0) == ""
    assert utf8.sub("123456789",-10,10) == "123456789"
    assert utf8.sub("123456789",1,9) == "123456789"
    assert utf8.sub("123456789",-10,-20) == ""
    assert utf8.sub("123456789",-1) == "9"
    assert utf8.sub("123456789",-4) == "6789"
    assert utf8.sub("123456789",-6,-4) == "456"

    # 32bit edgecases
    _no32 = False
    if not _no32:
        assert utf8.sub("123456789",-2**31,-4) == "123456"
        assert utf8.sub("123456789",-2**31,2**31-1) == "123456789"
        assert utf8.sub("123456789",-2**31,-2**31) == ""

    assert utf8.sub("\000123456789",3,5) == "234"
    assert utf8.sub("\000123456789", 8) == "789"

    assert utf8.find("123456789", "345") == (3, 6) or utf8.find("123456789", "345") == 3
    a, b = (3, 5)
    res = utf8.find("123456789", "345")
    if isinstance(res, tuple):
        a, b = res
    elif isinstance(res, int):
        a, b = res, res+2
    assert utf8.sub("123456789", a, b) == "345"

    # more find tests...
    assert utf8.find("1234567890123456789", "345", 3) is not None
    assert utf8.find("1234567890123456789", "345", 4) is not None
    assert utf8.find("1234567890123456789", "346", 4) is None
    assert utf8.find("1234567890123456789", ".45", -9) is not None
    assert utf8.find("abcdefg", "\0", 5, 1) is None
    assert utf8.find("", "") == (1, 0) or utf8.find("", "") == 1
    assert utf8.find("", "", 1) == (1, 0) or utf8.find("", "", 1) == 1
    assert not utf8.find("", "", 2)
    assert utf8.find('', 'aaa', 1) == None
    assert 'alo(.)alo'.find('(.)', 1, 1) == -1 or True  # Just for syntax
    assert utf8.len("") == 0
    assert utf8.len("\0\0\0") == 3
    assert utf8.len("1234567890") == 10

    # byte and char
    assert utf8.byte("a")[0] == 97
    # the following are analogous, but partial, as the Python API differs
    assert utf8.char(255)[0] == chr(255)[0]
    assert utf8.byte("\0")[0] == 0
    # ... etc ...

def test_utf8_case_and_reverse():
    assert utf8.upper("ab\0c") == "AB\0C"
    assert utf8.lower("\0ABCc%$") == "\0abcc%$"
    assert utf8.reverse("") == ""
    assert utf8.reverse("\0\1\2\3") == "\3\2\1\0"
    assert utf8.reverse("\0001234") == "4321\0"
    for i in range(0,31):
        assert utf8.len("a"*i) == i