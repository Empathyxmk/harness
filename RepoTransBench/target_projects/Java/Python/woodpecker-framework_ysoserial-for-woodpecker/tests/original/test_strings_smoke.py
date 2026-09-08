# Translated from StringsSmokeTest.java

import pytest

class Strings:
    @staticmethod
    def is_empty(value):
        return value is None or value == ""

    @staticmethod
    def is_not_empty(value):
        return value is not None and value != ""

    @staticmethod
    def repeat(val, n):
        return val * n if val and n > 0 else ""

def test_is_empty():
    assert Strings.is_empty(None) is True
    assert Strings.is_empty("") is True
    assert Strings.is_empty("abc") is False

def test_is_not_empty():
    assert Strings.is_not_empty(None) is False
    assert Strings.is_not_empty("") is False
    assert Strings.is_not_empty("value") is True

def test_repeat():
    assert Strings.repeat("x", 0) == ""
    assert Strings.repeat("x", 3) == "xxx"
    assert Strings.repeat("foobar", 2) == "foobarfoobar"