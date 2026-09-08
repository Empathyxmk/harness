import pytest
from openwifipass import Connection

class DummyPWSHandlerPublic:
    def __init__(self):
        self.calls = []
    def receivePWS2(self, x): self.calls.append(("pws2", x))
    def receiveM2(self, x): self.calls.append(("m2", x))
    def receiveM4(self, x): self.calls.append(("m4", x))
    def receivePWS4(self, x): self.calls.append(("pws4", x))

@pytest.mark.parametrize("ft,state,exp", [
    (25, 0, "pws2"),    # PWS1 (different frame type)
    (20, 1, "m2"),      # M2 after PWS1 (different frame type)
    (20, 2, "m4"),      # M4 after M2 (different frame type)
    (7,  3, "pws4"),    # PWS4 after M4 (different frame type)
])
def test_handleNotification_main_paths_public(ft, state, exp):
    handler = DummyPWSHandlerPublic()
    d = Connection.WPNearbyReadDelegate(handler)
    d.state = state
    d.openFrame = True
    pl = bytes([ft,99]) + b"other"
    d.payload = list(pl)
    d.expectedPayloadLength = len(pl)
    d.handleNotification(None, b"")
    assert handler.calls and handler.calls[0][0] == exp

def test_handleNotification_triggers_warning_public(monkeypatch):
    handler = DummyPWSHandlerPublic()
    d = Connection.WPNearbyReadDelegate(handler)
    d.state = 0
    d.openFrame = True
    pl = bytes([0xF0,42]) + b"abc"
    d.payload = list(pl)
    d.expectedPayloadLength = len(pl)
    called = {}
    def warn(msg): called['w'] = msg
    monkeypatch.setattr(Connection.logger, "warning", warn)
    d.handleNotification(None, b"")
    assert 'w' in called

def test_handleNotification_open_newframe_public():
    handler = DummyPWSHandlerPublic()
    d = Connection.WPNearbyReadDelegate(handler)
    d.state = 0
    d.openFrame = False
    data = bytes([0x08, 0x00]) + b"xyz"
    d.handleNotification(None, data)
    assert d.openFrame is True
    assert d.expectedPayloadLength == 4
    assert d.payload == b"xyz"

def test_handleNotification_frame_completion_public():
    handler = DummyPWSHandlerPublic()
    d = Connection.WPNearbyReadDelegate(handler)
    d.state = 0
    d.openFrame = False
    frameType = 25
    serviceType = 2
    payload = bytes([frameType, serviceType]) + b"info"
    expLen = len(payload)
    data = expLen.to_bytes(2, "little") + payload
    d.handleNotification(None, data)
    assert handler.calls and handler.calls[0][0] == "pws2"

def test_startPWS_does_not_crash_public(monkeypatch):
    monkeypatch.setattr(Connection, "GrantorHandler", lambda ssid, psk: type('X', (), {"sendPWS1": lambda self: None})())
    class FakePeripheral:
        def __init__(self, addr, type): pass
        def setDelegate(self, d): self.d = d
        def getServiceByUUID(self, uuid):
            class S:
                def getCharacteristics(self, forUUID): 
                    class C:
                        def getHandle(self): return 9
                    return [C()]
            return S()
        def writeCharacteristic(self, handle, value, withResponse): self.wc = (handle, value)
        def waitForNotifications(self, tout):
            if not hasattr(self, 'notcalled'):
                self.notcalled = True
                return True
            return False
        def disconnect(self): self.disc = True
    monkeypatch.setattr(Connection, "Peripheral", FakePeripheral)
    monkeypatch.setattr(Connection, "ADDR_TYPE_RANDOM", None)
    Connection.startPWS("address456", "ssid2", "psk2")  # No assert, just coverage