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
    assert to_upper("abc") == "ABC"
    assert to_upper("AbC123") == "ABC123"
    assert to_upper("") == ""

def test_starts_with():
    assert starts_with("abcdef", "abc")
    assert not starts_with("abcdef", "de")
    assert starts_with("abc", "")
    assert not starts_with("", "a")
    assert starts_with("", "")

def test_ends_with():
    assert ends_with("abcdef", "ef")
    assert not ends_with("abcdef", "de")
    assert ends_with("abc", "")
    assert not ends_with("", "a")
    assert ends_with("", "")

def test_replace_all():
    s = "abc abc"
    s2 = replace_all(s, "a", "x")
    assert s2 == "xbc xbc"

    s = "aaaa"
    s2 = replace_all(s, "aa", "b")
    assert s2 == "bb"

    s = "nothing"
    s2 = replace_all(s, "z", "!")
    assert s2 == "nothing"