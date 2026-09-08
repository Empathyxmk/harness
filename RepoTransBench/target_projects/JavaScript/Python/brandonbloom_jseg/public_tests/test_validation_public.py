import pytest

def is_valid_id(val):
    # For the sake of the test: a valid ID is an alphanumeric string (no whitespace)
    # and at least 1 character
    return isinstance(val, str) and val.isidentifier()

def is_valid_scalar(val):
    # Accepts int, float, str, bool, None
    return isinstance(val, (int, float, str, bool)) or val is None

def test_valid_ids():
    assert is_valid_id("foo")
    assert is_valid_id("bar123")
    assert not is_valid_id("with space")
    assert not is_valid_id("")
    assert not is_valid_id("!@#")
    assert not is_valid_id(123)
    assert not is_valid_id(None)

def test_valid_scalar():
    assert is_valid_scalar(123)
    assert is_valid_scalar(3.14)
    assert is_valid_scalar("string!")
    assert is_valid_scalar(True)
    assert is_valid_scalar(None)
    assert not is_valid_scalar([1,2,3])
    assert not is_valid_scalar({"a":1})

def test_edge_cases():
    assert not is_valid_id("123abc")  # Leading digits not valid as identifier
    assert is_valid_id("_fooBar")
    assert not is_valid_id("foo-bar")
    assert not is_valid_id("foo.bar")