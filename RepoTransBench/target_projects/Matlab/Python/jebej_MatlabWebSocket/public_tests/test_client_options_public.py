import pytest

class WebSocketClient:
    def __init__(self, url, protocols=None, **kwargs):
        self.url = url
        self.protocols = protocols
        self.opts = kwargs

def test_set_options_public():
    sc = WebSocketClient('ws://foo:9000', ['protocolX'], userFlag=True, userOption=123)
    assert isinstance(sc, WebSocketClient)