import pytest

class WebSocketClient:
    def __init__(self, url, protocols=None, **kwargs):
        self.url = url
        self.protocols = protocols
        self.opts = kwargs

def test_set_options():
    sc = WebSocketClient('ws://localhost:9000', ['protocol'], myFlag=True)
    assert isinstance(sc, WebSocketClient)