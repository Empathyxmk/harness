import pytest

class WebSocketConnection:
    def __init__(self, id, arg):
        self.ID = id
        self.extra = arg

def test_core_props():
    wsc = WebSocketConnection('id', [])
    assert wsc.ID == 'id'