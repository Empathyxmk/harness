import pytest
from src import pystring

def test_pystring_public_startswith():
    assert pystring.startswith("dogwood", "dog")
    assert not pystring.startswith("dogwood", "cat")
    assert pystring.startswith("racecar", "")

def test_pystring_public_endswith():
    assert pystring.endswith("helloearth", "earth")
    assert not pystring.endswith("helloearth", "mars")
    assert pystring.endswith("space", "")

def test_pystring_public_find():
    assert pystring.find("pineapple", "apple") == 4
    assert pystring.find("pineapple", "berry") == -1
    assert pystring.find("sphere", "") == 0

def test_pystring_public_index():
    pystring.index("blueberry", "berry")  # Should not raise
    with pytest.raises(ValueError):
        pystring.index("blueberry", "orange")  # Should raise

def test_pystring_public_strip():
    assert pystring.strip("   owl   ") == "owl"
    assert pystring.strip("***banana***", "*") == "banana"
    assert pystring.strip(" cherry ") == "cherry"