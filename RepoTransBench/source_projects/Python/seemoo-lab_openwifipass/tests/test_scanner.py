import pytest
from openwifipass.Scanner import PWSScanner

class DummyTLVBox:
    def __init__(self, d):
        self._d = d
    def toDict(self):
        return self._d

class DummyScanEntry:
    def __init__(self):
        self.addr = "AA:BB:01:FA:EE:DC"
        self.scan_data = []
    def getScanData(self):
        return self.scan_data

def test_getpwstlv_wrong_company(monkeypatch):
    scanner = PWSScanner("testssid")
    assert scanner.getPWSTLV(b"\x00\x00ABC") is None

def test_getpwstlv_right_company(monkeypatch):
    # Patch TLV8Box.decodeFromData to return a DummyTLVBox
    monkeypatch.setattr("openwifipass.Scanner.TLV8Box.decodeFromData", lambda d: DummyTLVBox({0x0F: b'PAYLOAD'}))
    scanner = PWSScanner("testssid")
    result = scanner.getPWSTLV(bytes.fromhex("4c00abcdef"))
    assert result == b'PAYLOAD'

def test_isssidintlv():
    scanner = PWSScanner("SSID42")
    # last 3 bytes override
    val = scanner.ssidHash[:3]
    # Build input so last 3 bytes match ssidHash[:3], earlier content doesn't affect
    assert scanner.isSSIDInTLV(b"xxxx" + val) is True
    # Input that does NOT match last 3 bytes, checking for correct logic
    assert scanner.isSSIDInTLV(b"abc123") is False

def test_handleDiscovery_sets_result(monkeypatch):
    # Provide getPWSTLV returns matching TLV
    class DummyScan:
        def __init__(self):
            self.addr = "Z"
        def getScanData(self):
            # adtype 255 (manufacturer), value is hex
            return [(255, None, "4c00abcdef")]
    scanner = PWSScanner("ssidX")
    # Patch getPWSTLV to return something that matches isSSIDInTLV
    def fake_getPWSTLV(data):
        return scanner.ssidHash[:3] + scanner.ssidHash[:3]
    scanner.getPWSTLV = fake_getPWSTLV
    scanner.isSSIDInTLV = lambda tlv: True
    scanEntry = DummyScan()
    scanner.handleDiscovery(scanEntry, True, True)
    assert scanner.result is scanEntry

def test_handleDiscovery_nonmatching(monkeypatch):
    class DummyScan:
        def getScanData(self):
            return [(255, None, "4c00abcdef")]
    scanner = PWSScanner("ssid")
    scanner.getPWSTLV = lambda data: None
    scanner.handleDiscovery(DummyScan(), True, True)
    assert scanner.result is None