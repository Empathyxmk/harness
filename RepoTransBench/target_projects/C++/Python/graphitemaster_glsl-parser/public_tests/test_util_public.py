import pytest

def test_alloc_fmt_different():
    # Simulate allocation and formatting
    s = "Hello %s, pi is %.2f" % ("Alice", 3.14)
    assert s == "Hello Alice, pi is 3.14"
    assert len(s) == len("Hello Alice, pi is 3.14")

def test_alloc_fmt_empty_different():
    s = " "
    assert s == " "
    assert len(s) == 1

def test_alloc_fmt_just_string_different():
    s = "Another test string"
    assert s == "Another test string"
    assert len(s) == len("Another test string")

def test_alloc_fmt_large_string_different():
    long_str = "1234567890_abcdefghijklmnopqrstuvwxyz_1234567890_abcdefghijklmnopqrstuvwxyz_"
    s = "%s%s" % (long_str, long_str)
    assert len(s) == len(long_str) * 2
    expected = long_str + long_str
    assert s == expected

def test_alloc_v_fmt_different():
    val = 255
    s = "Hex: %x" % val
    assert s == "Hex: ff"
    assert len(s) == len("Hex: ff")