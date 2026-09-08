import pytest

class WebSocketConnection:
    def __init__(self, id, arg):
        self.ID = id
        self.extra = arg
    def toupper(self, msg):
        return str(msg).upper()

def test_misc_methods():
    wsc = WebSocketConnection('test_id', [])
    assert wsc.ID == 'test_id'
    outmsg = wsc.toupper('hello')
    assert outmsg == 'HELLO'