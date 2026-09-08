import pytest

class WebSocketClient:
    def __init__(self, url, protocols=None, **kwargs):
        self.url = url
        self.protocols = protocols
        self.opts = kwargs
        self.is_open = False
    def open(self):
        self.is_open = True
    def close(self):
        self.is_open = False

def test_repeat_open():
    c = WebSocketClient('ws://localhost:9999')
    c.open()
    c.close()
    c.open()
    c.close()
    assert True  # if no exception, test passes