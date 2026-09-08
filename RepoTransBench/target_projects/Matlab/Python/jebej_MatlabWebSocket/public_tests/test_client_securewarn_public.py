import pytest

class WebSocketClient:
    def __init__(self, url, protocols=None, **kwargs):
        self.url = url
        self.protocols = protocols
        self.opts = kwargs

def test_warning_on_insecure_cert_public():
    c = WebSocketClient('wss://example.com:9943', {}, AllowInsecure=True)
    assert isinstance(c, WebSocketClient)