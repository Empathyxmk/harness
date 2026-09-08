import pytest

class WSExample:
    def call(self):
        return "Result from WS call"

def test_ws_call_public():
    ws = WSExample()
    result = ws.call()
    assert result is not None
    assert result != ""