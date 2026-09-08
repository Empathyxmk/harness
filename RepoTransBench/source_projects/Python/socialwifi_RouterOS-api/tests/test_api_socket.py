import pytest
import socket
from routeros_api import api_socket, exceptions

class DummySock:
    def __init__(self):
        self.closed = False
        self.timeout = None
        self.sent_data = None
    def close(self):
        self.closed = True
    def settimeout(self, timeout):
        self.timeout = timeout
    def sendall(self, data):
        self.sent_data = data
        return None
    def recv(self, length):
        return b'ABC'[0:length]

def test_set_keepalive_sets_options(monkeypatch):
    sock = DummySock()
    monkeypatch.setattr(socket, 'SO_KEEPALIVE', 999, raising=False)
    monkeypatch.setattr(socket, 'SOL_SOCKET', 998, raising=False)
    monkeypatch.setattr(socket, 'IPPROTO_TCP', 997, raising=False)
    monkeypatch.setattr(socket, 'TCP_KEEPIDLE', 1, raising=False)
    monkeypatch.setattr(socket, 'TCP_KEEPINTVL', 2, raising=False)
    monkeypatch.setattr(socket, 'TCP_KEEPCNT', 3, raising=False)
    sock.setsockopt = lambda *a, **kw: None
    api_socket.set_keepalive(sock)

def test_dummy_socket_methods():
    s = api_socket.DummySocket()
    assert s.close() is None
    assert s.settimeout(10) is None

def test_socket_wrapper_send_receive_close():
    ds = DummySock()
    sw = api_socket.SocketWrapper(ds)
    sw.send(b'hi')
    assert ds.sent_data == b'hi'
    out = sw.receive(2)
    assert out == b'AB'
    sw.close()
    assert ds.closed
    sw.settimeout(5)
    assert ds.timeout == 5

def test_socket_wrapper_receive_connection_closed(monkeypatch):
    class E(Exception): pass
    class Closer(DummySock):
        def recv(self, length):
            return b''
    sw = api_socket.SocketWrapper(Closer())
    with pytest.raises(exceptions.RouterOsApiConnectionClosedError):
        sw.receive(2)

def test_socket_wrapper_receive_eintr(monkeypatch):
    class E(Exception): pass
    class EiSock(DummySock):
        def __init__(self):
            super().__init__()
            self.called = False
        def recv(self, length):
            if not self.called:
                self.called = True
                raise socket.error(getattr(api_socket, 'EINTR', 4), 'test')
            return b'AB'
    sw = api_socket.SocketWrapper(EiSock())
    assert sw.receive(2) == b'AB'