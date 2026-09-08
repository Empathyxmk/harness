import pytest

class StorageProperties:
    def __init__(self):
        self._location = "uploads"
    def getLocation(self):
        return self._location
    def setLocation(self, loc):
        self._location = loc

def test_default_location():
    properties = StorageProperties()
    assert properties.getLocation() == "uploads"

def test_set_location():
    properties = StorageProperties()
    properties.setLocation("abc")
    assert properties.getLocation() == "abc"