import pytest

def to_upper(input_):
    return input_.upper()

def starts_with(value, start):
    if len(start) > len(value):
        return False
    return value.startswith(start)

def ends_with(value, end):
    if len(end) > len(value):
        return False
    return value.endswith(end)

def replace_all(subject, search, replace):
    return subject.replace(search, replace)

def test_to_upper():
    assert to_upper("xyz") == "XYZ"
    assert to_upper("TestCASE") == "TESTCASE"
    assert to_upper("123abc!") == "123ABC!"
    assert to_upper("abcxyz") == "ABCXYZ"

def test_starts_with():
    assert starts_with("hello, world", "hello")
    assert not starts_with("goodbye", "bye")
    assert starts_with("foo", "")
    assert not starts_with("", "nonempty")
    assert starts_with("", "")

def test_ends_with():
    assert ends_with("superman", "man")
    assert not ends_with("superwoman", "manly")
    assert ends_with("baz", "")
    assert not ends_with("", "foo")
    assert ends_with("", "")

def test_replace_all():
    s = "nom nom pizza"
    s2 = replace_all(s, "nom", "yum")
    assert s2 == "yum yum pizza"

    s = "bbbb"
    s2 = replace_all(s, "bb", "a")
    assert s2 == "aa"

    s = "applepie"
    s2 = replace_all(s, "z", "!")
    assert s2 == "applepie"