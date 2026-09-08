import pytest

class KeyChainClass:
    def __init__(self):
        self._key = ""
        self._password = ""

    def setKey(self, key):
        self._key = key

    def getKey(self):
        return self._key

    def setPassword(self, password):
        self._password = password

    def getPassword(self):
        return self._password

def test_keychainclass_workflow():
    kc = KeyChainClass()
    kc.setKey("test_key")
    kc.setPassword("test_pass")
    assert kc.getKey() == "test_key"
    assert kc.getPassword() == "test_pass"

    kc.setKey("")
    kc.setPassword("")
    assert kc.getKey() == ""
    assert kc.getPassword() == ""

    kc.setKey("another_key")
    kc.setPassword("another_pass")
    assert kc.getKey() == "another_key"
    assert kc.getPassword() == "another_pass"