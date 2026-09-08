import pytest
from openwifipass import GrantorHandler

def test_getSSID_public():
    handler = GrantorHandler.GrantorHandler("AnotherSSID", "AnotherSecretPSK")
    assert handler.getSSID() == "AnotherSSID"

def test_getPSK_public():
    handler = GrantorHandler.GrantorHandler("PublicSSID", "DifferentPSKValue")
    assert handler.getPSK() == "DifferentPSKValue"

def test_getSharedSecret_public():
    handler = GrantorHandler.GrantorHandler("abc", "def")
    # Should produce bytes of length 32
    secret = handler.getSharedSecret()
    assert isinstance(secret, bytes)
    assert len(secret) == 32

def test_checkSharedSecret_public():
    handler = GrantorHandler.GrantorHandler("SSID1", "PSK1")
    real_secret = handler.getSharedSecret()
    assert handler.checkSharedSecret(real_secret)
    # Pass in incorrect secret, should be False
    assert handler.checkSharedSecret(b"x" * 32) is False