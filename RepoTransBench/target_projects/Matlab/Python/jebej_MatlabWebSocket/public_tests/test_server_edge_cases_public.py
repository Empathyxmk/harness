import pytest

class WebSocketServer:
    def __init__(self, port):
        self.port = port
        self.running = True
    def stop(self):
        self.running = False
    def start(self):
        self.running = True

def test_start_stop_server_public():
    s = WebSocketServer(12399)
    try:
        s.stop()
        s.stop()
        s.start()
        s.stop()
        assert True
    except Exception as err:
        pytest.fail(f'Server edge failed: {err}')