import pytest

class DummyPrefs:
    def __init__(self):
        self.store = {}
    def edit(self):
        return self
    def putString(self, k, v):
        self.store[k] = v
        return self
    def apply(self):
        return True
    def getString(self, k, default=None):
        return self.store.get(k, default)

class SecurityUtils:
    @staticmethod
    def encrypt(value):
        # simple mock encryption (reverse string + "ENCRYPTED")
        return value[::-1] + "_ENCRYPTED"

class Preference_UserDevice:
    def __init__(self):
        self.preferences = DummyPrefs()
        self._version = None
        self._uuid = None
    @staticmethod
    def getInstance(context=None):
        return Preference_UserDevice()
    def getEntityName(self):
        return "Preference_UserDevice"
    def versionKeyName(self): return "version"
    def uuidKeyName(self): return "uuid"
    def getVersion(self): return self._version
    def getUuid(self):
        # simulate decryption; reverse encryption for test
        if not self._uuid:
            return None
        return self._uuid
    def putUuid(self, uuid):
        self._uuid = uuid
        self.preferences.putString("uuid", SecurityUtils.encrypt(uuid))
    def putVersion(self, v):
        self._version = v
        self.preferences.putString(self.versionKeyName(), v)

@pytest.fixture(scope="function")
def device():
    return Preference_UserDevice.getInstance()

def test_version(device):
    version = "1.0.0.0"
    device.preferences.putString(device.versionKeyName(), version).apply()
    device._version = version
    assert device.getVersion() == version

def test_security(device):
    uuid = "00001234-0000-0000-0000-000123456789"
    device.putUuid(uuid)
    assert device.getUuid() == uuid
    assert device.preferences.getString("uuid") == SecurityUtils.encrypt(uuid)