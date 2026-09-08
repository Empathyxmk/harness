import pytest

def test_string_conversion():
    fixtures = [bytes([0, 127, 128, 255]), bytearray([0, 127, 128, 255])]
    for value in fixtures:
        value_type = type(value)
        returned_value = value_type(value)
        assert isinstance(returned_value, value_type)
        assert returned_value == value