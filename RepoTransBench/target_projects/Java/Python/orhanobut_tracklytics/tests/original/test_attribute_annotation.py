import pytest

class Attribute:
    def __init__(self, value='', defaultValue='', isSuper=False):
        self.value = value
        self.defaultValue = defaultValue
        self.isSuper = isSuper

def test_attribute_values():
    attr = Attribute(value="val", defaultValue="def", isSuper=True)
    assert attr.value == "val"
    assert attr.defaultValue == "def"
    assert attr.isSuper is True

def test_attribute_default_is_super_and_default_value():
    attr = Attribute(value="key")
    assert attr.value == "key"
    assert attr.defaultValue == ""
    assert attr.isSuper is False