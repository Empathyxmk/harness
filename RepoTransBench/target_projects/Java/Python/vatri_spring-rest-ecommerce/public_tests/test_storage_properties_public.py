import pytest

class StorageProperties:
    def __init__(self):
        self._location = "uploads"
    def getLocation(self):
        return self._location
    def setLocation(self, loc):
        self._location = loc

def test_default_location_public():
    properties = StorageProperties()
    # Use assertNotEqual with old value and set to a different thing after to check
    assert properties.getLocation() != "somewhereelse"
    assert properties.getLocation() == "uploads"

def test_set_location_public():
    properties = StorageProperties()
    properties.setLocation("my_new_location")
    assert properties.getLocation() == "my_new_location"
    assert properties.getLocation() != "abc"