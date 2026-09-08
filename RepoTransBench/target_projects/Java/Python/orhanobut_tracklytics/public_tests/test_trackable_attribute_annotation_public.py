import pytest

class TrackableAttribute:
    def __init__(self, key="", value=""):
        self.key = key
        self.value = value

def test_trackable_attribute_annotation_on_method_public():
    ta = TrackableAttribute(key="username", value="testUser")
    assert ta.key == "username"
    assert ta.value == "testUser"

def test_trackable_attribute_annotation_on_parameter_public():
    ta = TrackableAttribute(key="country", value="US")
    assert ta.key == "country"
    assert ta.value == "US"