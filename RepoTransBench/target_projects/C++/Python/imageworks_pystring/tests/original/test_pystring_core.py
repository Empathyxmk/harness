import pytest
from src import pystring

def test_pystring_startswith():
    assert pystring.startswith("foobar", "foo")
    assert not pystring.startswith("foobar", "bar")
    assert pystring.startswith("foobar", "")

def test_pystring_endswith():
    assert pystring.endswith("foobar", "bar")
    assert not pystring.endswith("foobar", "foo")
    assert pystring.endswith("foobar", "")

def test_pystring_find():
    assert pystring.find("hello world", "world") == 6
    assert pystring.find("hello world", "mars") == -1
    assert pystring.find("xyz", "") == 0

def test_pystring_index():
    # "world" IS found, so no exception
    pystring.index("hello world", "world")
    # "mars" NOT found, should throw
    with pytest.raises(ValueError):
        pystring.index("hello world", "mars")

def test_pystring_strip():
    assert pystring.strip("   test   ") == "test"
    assert pystring.strip("***abc***", "*") == "abc"
    assert pystring.strip(" xyz ") == "xyz"