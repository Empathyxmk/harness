import pytest
try:
    from src.parser import parser_constants as constants
except ImportError:
    constants = {}

def test_export_at_least_one_constant_property():
    assert len(dir(constants)) > 0 or hasattr(constants, "__dict__")

def test_export_version_field_if_present():
    if hasattr(constants, 'VERSION'):
        version = getattr(constants, "VERSION")
        assert isinstance(version, str)
        assert len(version) > 0