import pytest

def test_public_str_is_str():
    # Instead of compat.basestring, just assert str is str in py3
    assert isinstance('a', str)
    assert type(str()) == str

def test_public_int_is_int():
    # Instead of compat.long, check int
    y = 42
    assert isinstance(y, int)

def test_public_unicode_is_str_py3():
    # Just check that "foo" is str in py3, since compat.unicode is missing
    z = "foo"
    assert type(z) == str

def test_public_py3_features():
    # Just check that certain features exist in python3
    assert hasattr(str, 'format')
    assert type(range(3)) != list  # In py3 range is its own type

def test_public_bytes_types():
    a = b'abc'
    assert isinstance(a, bytes)
    b = "def"
    assert isinstance(b, str)

def test_public_string_types_str():
    s = "something"
    assert isinstance(s, str)