from unittest import TestCase

from routeros_api import api_socket

try:
    from unittest import mock
except ImportError:
    import mock

class TestApiSocketPublic(TestCase):
    def test_socket_init_and_close(self):
        sock = mock.Mock()
        conn = api_socket.ApiSocket(sock)
        conn.socket = sock
        conn.close()
        sock.close.assert_called_once()

    def test_is_alive_alive_and_dead(self):
        sock = mock.Mock()
        conn = api_socket.ApiSocket(sock)
        conn.is_alive = True
        self.assertTrue(conn.is_alive)
        conn.is_alive = False
        self.assertFalse(conn.is_alive)