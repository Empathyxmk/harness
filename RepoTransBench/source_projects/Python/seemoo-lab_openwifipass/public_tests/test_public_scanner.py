import hashlib
import types
import pytest
from openwifipass import Scanner

class DummyScanEntry:
    def __init__(self, addr, scan_data):
        self.addr = addr
        self._scan_data = scan_data
    def getScanData(self):
        return self._scan_data

def test_getPWSTLV_and_isSSIDInTLV_public():
    ssid = "DifferentSSID"
    s = Scanner.PWSScanner(ssid)
    company_id = Scanner.BLE_COMPANY_ID_APPLE
    # The TLV8Box decodeFromData method expects bytes after Apple ID.
    # We'll fudge up a TLV8Box interface for public test with public data.
    # The test will cover getPWSTLV and isSSIDInTLV.
    # Provide fake TLV8Box for monkeypatch.
    class FakeBox:
        def toDict(self):
            # Tag 0x0F key expected by getPWSTLV
            return {0x0F: b"something" + s.ssidHash[:3]}
    fake_bytes = b"notused"

    monkeyed = {}
    def fake_decodeFromData(data):
        monkeyed['called'] = True
        return FakeBox()
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr("openwifipass.TLV8.TLV8Box.decodeFromData", fake_decodeFromData)
    tlv = s.getPWSTLV(company_id + fake_bytes)
    assert monkeyed['called']
    assert s.isSSIDInTLV(tlv) is True
    monkeypatch.undo()

def test_handleDiscovery_sets_result_public(monkeypatch):
    ssid = "wowPublicSSID"
    s = Scanner.PWSScanner(ssid)
    kc = Scanner.BLE_COMPANY_ID_APPLE
    # encode ssid hash at end so isSSIDInTLV checks last 3 bytes
    dummy_tlv_val = b"bonusbytes" + s.ssidHash[:3]
    class FakeBox:
        def toDict(self): return {0x0F: dummy_tlv_val}
    def fake_decodeFromData(data): return FakeBox()
    monkeypatch.setattr("openwifipass.TLV8.TLV8Box.decodeFromData", fake_decodeFromData)
    # adtype 255 = BLE_MANUFACTURER_DATA
    scan_entry = DummyScanEntry("AA:BB:PP:UU:BL:1C", [(255, None, (kc + b"xyz").hex())])
    s.handleDiscovery(scan_entry, True, True)
    assert s.result == scan_entry
    monkeypatch.undo()