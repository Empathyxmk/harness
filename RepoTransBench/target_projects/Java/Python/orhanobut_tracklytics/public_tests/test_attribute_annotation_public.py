import pytest

class Attribute:
    def __init__(self, value='', defaultValue='', isSuper=False):
        self.value = value
        self.defaultValue = defaultValue
        self.isSuper = isSuper

def test_attribute_annotation_public_present():
    attr = Attribute(value="pubKey", defaultValue="pubDefault", isSuper=True)
    assert attr.value == "pubKey"
    assert attr.defaultValue == "pubDefault"
    assert attr.isSuper is True

def test_parameter_annotation_public_present():
    attr = Attribute(value="pubParam")
    assert attr.value == "pubParam"