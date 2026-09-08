import pytest

class WebSocketConnection:
    def __init__(self, id, arg):
        self.ID = id
        self.extra = arg

def test_core_props_public():
    wsc = WebSocketConnection('idX', [])
    assert wsc.ID == 'idX'