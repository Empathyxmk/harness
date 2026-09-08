import pytest
import importlib

# Dynamic import of class from module since not imported into __init__.py
GrantorHandler_mod = importlib.import_module("openwifipass.GrantorHandler")
PWSGrantorHandler = getattr(GrantorHandler_mod, "PWSGrantorHandler", None)

@pytest.mark.skipif(PWSGrantorHandler is None, reason="PWSGrantorHandler not exposed at module level")
def test_handler_creation():
    handler = PWSGrantorHandler()
    assert isinstance(handler, PWSGrantorHandler)

@pytest.mark.skipif(PWSGrantorHandler is None, reason="PWSGrantorHandler not exposed at module level")
def test_parse_request_wrong_type():
    handler = PWSGrantorHandler()
    # Should handle wrong type gracefully
    result = handler.parseRequest({"type": 1000, "payload": "random"})
    assert result is None

@pytest.mark.skipif(PWSGrantorHandler is None, reason="PWSGrantorHandler not exposed at module level")
def test_get_ssid():
    handler = PWSGrantorHandler()
    # Without a session, should return None
    assert handler.getSSID() is None

@pytest.mark.skipif(PWSGrantorHandler is None, reason="PWSGrantorHandler not exposed at module level")
def test_get_password():
    handler = PWSGrantorHandler()
    # Without a session, should return None
    assert handler.getPassword() is None

@pytest.mark.skipif(PWSGrantorHandler is None, reason="PWSGrantorHandler not exposed at module level")
def test_authorize():
    handler = PWSGrantorHandler()
    # Should just return True (open WiFi is always authorized)
    assert handler.authorize() is True

@pytest.mark.skipif(PWSGrantorHandler is None, reason="PWSGrantorHandler not exposed at module level")
def test_methods_default(monkeypatch):
    handler = PWSGrantorHandler()
    monkeypatch.setattr(handler, "session", type("obj", (object,), {})())
    setattr(handler.session, "ssid", "myssid")
    setattr(handler.session, "password", "pw")
    assert handler.getSSID() == "myssid"
    assert handler.getPassword() == "pw"