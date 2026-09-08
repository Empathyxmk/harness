import pytest

class WebSocketConnection:
    def __init__(self, id, arg):
        self.ID = id
        self.extra = arg
    def toupper(self, msg):
        return str(msg).upper()

def test_misc_methods_public():
    wsc = WebSocketConnection('test_id_public', [])
    assert wsc.ID == 'test_id_public'
    outmsg = wsc.toupper('abcde')
    assert outmsg == 'ABCDE'