import pytest
from bumpversion.version_part import VersionPart

def test_public_version_part_value_setting():
    vp = VersionPart("7", None, None)
    assert str(vp) == "7"

def test_public_version_part_compare_different_values():
    vp1 = VersionPart("3", None, None)
    vp2 = VersionPart("10", None, None)
    assert vp1 != vp2

def test_public_version_part_equality_with_same_value():
    vp1 = VersionPart("hello", None, None)
    vp2 = VersionPart("hello", None, None)
    assert vp1 == vp2

def test_public_version_part_repr():
    vp = VersionPart("2024", None, None)
    assert "2024" in repr(vp)

def test_public_version_part_str_cast():
    vp = VersionPart(543, None, None)
    assert str(vp) == "543"

def test_public_version_part_int_cast():
    vp = VersionPart("8", None, None)
    assert int(vp) == 8

def test_public_version_part_int_cast_non_numeric():
    vp = VersionPart("xyz", None, None)
    with pytest.raises(ValueError):
        int(vp)