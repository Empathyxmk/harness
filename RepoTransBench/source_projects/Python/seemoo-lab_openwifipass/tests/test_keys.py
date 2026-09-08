import pytest
import importlib

Keys_mod = importlib.import_module("openwifipass.Keys")

def test_key_constants():
    assert getattr(Keys_mod, "BLE_MFG_ID", None) == 0x004C
    assert getattr(Keys_mod, "PWS_TYPE", None) == 0x0F

def test_get_ble_vendor():
    assert Keys_mod.get_ble_vendor() == 0x004C

def test_get_pws_type():
    assert Keys_mod.get_pws_type() == 0x0F

def test_session_keys():
    sk = Keys_mod.SessionKeys()
    assert sk.get() == "dummy_session_key"