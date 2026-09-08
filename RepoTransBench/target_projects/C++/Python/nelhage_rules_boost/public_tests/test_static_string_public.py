import pytest

def test_static_string_public():
    s1 = "abcdefg"[:4]
    assert s1 == "abcd"