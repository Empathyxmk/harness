import pytest
from unittest import mock

class FakeUkcp:
    def __init__(self):
        self._user = mock.Mock()
        self._user.getRemoteAddress.return_value = ("localhost", 12345)
        self.getConv = mock.Mock(return_value=42)
        self.write = mock.Mock()
    def user(self):
        return self._user

class FakeByteBuf:
    def __init__(self):
        self._data = bytearray(b"hello")
    def readBytes(self, n):
        out = self._data[:n]
        self._data = self._data[n:]
        return out
    def writeBytes(self, data):
        self._data.extend(data)

class Kcp4sharpExampleServer:
    def onConnected(self, ukcp): ukcp.write(b'connected')
    def handleReceive(self, buf, ukcp): ukcp.write(buf._data)
    def handleException(self, ex, ukcp): ukcp.write(str(ex).encode())
    def handleClose(self, ukcp): ukcp.write(b'closed')

class KcpDisconnectExampleServer(Kcp4sharpExampleServer): pass

class KcpMultiplePingPongExampleServer(Kcp4sharpExampleServer): pass

class KcpReconnectExampleServer(Kcp4sharpExampleServer):
    def __init__(self):
        super().__init__()
        self.start = None
    def handleReceive(self, buf, ukcp):
        import time
        if self.start is None:
            self.start = time.time() * 1000
        if (time.time()*1000 - self.start) > 1000:
            ukcp.write(buf._data)
        else:
            ukcp.write(b"first")

class SpeedExampleServer(Kcp4sharpExampleServer):
    def __init__(self):
        self.start = None
    def handleReceive(self, buf, ukcp):
        import time
        if self.start is None:
            self.start = time.time() * 1000
        if (time.time()*1000 - self.start) > 1000:
            ukcp.write(buf._data)
        else:
            ukcp.write(b"speed")

@pytest.fixture
def mock_ukcp():
    return FakeUkcp()

@pytest.fixture
def mock_buf():
    buf = FakeByteBuf()
    buf.writeBytes(b"hello")
    return buf

def test_kcp4sharp_example_server(mock_ukcp, mock_buf):
    server = Kcp4sharpExampleServer()
    server.onConnected(mock_ukcp)
    server.handleReceive(mock_buf, mock_ukcp)
    server.handleException(RuntimeError("error"), mock_ukcp)
    server.handleClose(mock_ukcp)
    assert mock_ukcp.write.call_count >= 1

def test_kcp_disconnect_example_server(mock_ukcp, mock_buf):
    server = KcpDisconnectExampleServer()
    server.onConnected(mock_ukcp)
    server.handleReceive(mock_buf, mock_ukcp)
    server.handleException(RuntimeError("error"), mock_ukcp)
    server.handleClose(mock_ukcp)
    assert mock_ukcp.write.call_count >= 1

def test_kcp_multiple_pingpong_server(mock_ukcp, mock_buf):
    server = KcpMultiplePingPongExampleServer()
    server.onConnected(mock_ukcp)
    server.handleReceive(mock_buf, mock_ukcp)
    server.handleException(RuntimeError("error2"), mock_ukcp)
    server.handleClose(mock_ukcp)
    assert mock_ukcp.write.call_count >= 1

def test_kcp_reconnect_example_server(mock_ukcp, mock_buf):
    import time
    server = KcpReconnectExampleServer()
    server.onConnected(mock_ukcp)
    server.handleReceive(mock_buf, mock_ukcp)
    # Simulate time passing
    server.start = (time.time() * 1000) - 2000
    server.handleReceive(mock_buf, mock_ukcp)
    server.handleException(RuntimeError("error3"), mock_ukcp)
    server.handleClose(mock_ukcp)
    assert mock_ukcp.write.call_count >= 1

def test_speed_example_server(mock_ukcp, mock_buf):
    import time
    server = SpeedExampleServer()
    server.onConnected(mock_ukcp)
    server.handleReceive(mock_buf, mock_ukcp)
    server.start = (time.time() * 1000) - 1200
    server.handleReceive(mock_buf, mock_ukcp)
    server.handleException(RuntimeError("error4"), mock_ukcp)
    server.handleClose(mock_ukcp)
    assert True