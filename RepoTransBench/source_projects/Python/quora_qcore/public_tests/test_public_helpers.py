import sys
import math
from qcore.helpers import all_equal, safe_unicode, clamp, safe_repr, str2bool
from qcore.asserts import assert_eq, assert_is, AssertRaises

def test_public_all_equal():
    assert_eq(all_equal([5, 5, 5]), True)
    assert_eq(all_equal([7, 6, 7]), False)
    assert_eq(all_equal([]), True)

def test_public_safe_unicode():
    s = safe_unicode(b"\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82")
    assert_eq(s, "Привет")
    s2 = safe_unicode("Simple string")
    assert_eq(s2, "Simple string")

def test_public_clamp():
    assert_eq(clamp(7, 3, 10), 7)
    assert_eq(clamp(2, 3, 10), 3)
    assert_eq(clamp(15, 3, 10), 10)

def test_public_safe_repr():
    class Strange:
        def __repr__(self):
            raise Exception("fail!")
    assert "fail!" in safe_repr(Strange())

def test_public_str2bool():
    assert_eq(str2bool('Yes'), True)
    assert_eq(str2bool('no'), False)
    assert_eq(str2bool('ON'), True)
    assert_eq(str2bool('0'), False)
    assert_eq(str2bool('false'), False)
    assert_eq(str2bool('yES'), True)

    with AssertRaises(ValueError):
        str2bool('maybe')