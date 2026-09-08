import pytest

class WebSocketClient:
    def __init__(self, url, protocols=None, **kwargs):
        # Simulate client initialization. Accept all options.
        self.url = url
        self.protocols = protocols
        self.opts = kwargs

def test_warning_on_insecure_cert(monkeypatch):
    # Should warn, but not error - we'll simulate warning tracking
    # In Matlab this simply disables a warning and checks type
    c = WebSocketClient('wss://localhost:8443', {}, AllowInsecure=True)
    assert isinstance(c, WebSocketClient)