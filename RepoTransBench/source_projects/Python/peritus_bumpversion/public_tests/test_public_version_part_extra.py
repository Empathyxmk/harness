import pytest
from bumpversion.version_part import VersionPart

def test_public_version_part_has_value():
    vp = VersionPart("nonempty", None, None)
    assert vp.has_value()

def test_public_version_part_not_has_value_empty_string():
    vp = VersionPart("", None, None)
    assert not vp.has_value()

def test_public_version_part_int_cast_zero():
    vp = VersionPart("0", None, None)
    assert int(vp) == 0

def test_public_version_part_ignore_value():
    vp = VersionPart("ignored", None, None)
    assert vp.value == "ignored"

def test_public_version_part_repr_contains_class():
    vp = VersionPart("classy", None, None)
    assert "VersionPart" in repr(vp)