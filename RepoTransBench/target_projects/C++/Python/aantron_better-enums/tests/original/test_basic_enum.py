import pytest
from enum import Enum

class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

    @classmethod
    def _from_string(cls, name):
        try:
            return cls[name]
        except KeyError:
            raise ValueError(f"No such enum value: {name}")

    @classmethod
    def _from_string_nothrow(cls, name):
        try:
            return cls[name]
        except KeyError:
            return None

    @classmethod
    def _values(cls):
        return list(cls)

    def _to_string(self):
        return self.name

def test_enum_name():
    c_red = Color.RED
    c_green = Color.GREEN
    c_blue = Color.BLUE

    assert c_red._to_string() == "RED"
    assert c_green._to_string() == "GREEN"
    assert c_blue._to_string() == "BLUE"

def test_enum_from_string():
    c1 = Color._from_string("GREEN")
    assert c1 == Color(Color.GREEN)

    c2 = Color._from_string_nothrow("BLUE")
    assert c2 is not None and c2 == Color(Color.BLUE)

    c3 = Color._from_string_nothrow("INVALID")
    assert c3 is None  # Should be None/False

def test_enum_value():
    assert Color.RED.value == 0
    assert Color.GREEN.value == 1
    assert Color.BLUE.value == 2

def test_enum_iteration():
    count = 0
    for e in Color._values():
        _ = e
        count += 1
    assert count == 3