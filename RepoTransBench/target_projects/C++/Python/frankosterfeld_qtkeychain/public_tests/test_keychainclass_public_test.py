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

def test_keychainclass_public():
    kc = KeyChainClass()
    kc.setKey("public_key")
    kc.setPassword("public_pass")
    assert kc.getKey() == "public_key"
    assert kc.getPassword() == "public_pass"

    kc.setKey("pub_empty")
    kc.setPassword("")
    assert kc.getKey() == "pub_empty"
    assert kc.getPassword() == ""

    kc.setKey("pubKey2")
    kc.setPassword("pubPass2")
    assert kc.getKey() == "pubKey2"
    assert kc.getPassword() == "pubPass2"