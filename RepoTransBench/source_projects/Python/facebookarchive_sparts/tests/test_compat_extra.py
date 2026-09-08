import pytest
import sparts.compat as compat

def test_basestring_py3():
    assert compat.basestring == str

def test_long_py3():
    assert compat.long == int

def test_unicode_py3():
    assert compat.unicode == str

def test_py_version_constants():
    # These should always be True for py3 in this repo
    assert compat.PY3
    assert not compat.PY2

def test_range_map_and_zip():
    # These should point to builtins in py3
    assert compat.range == range
    assert compat.map == map
    assert compat.zip == zip

def test_bytes_type_and_str_type():
    assert compat.bytes_type == bytes
    assert compat.str_type == str

def test_string_types_contains_str():
    assert str in compat.string_types
    assert isinstance("foo", compat.string_types)