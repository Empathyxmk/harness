from unittest import TestCase

try:
    from unittest import mock
except ImportError:
    import mock

from routeros_api import api_socket

class TestSocketPublic(TestCase):
    def test_socket_send_and_receive(self):
        sock = mock.Mock()
        api_socket_conn = api_socket.ApiSocket(sock)
        api_socket_conn.socket.send = mock.Mock(return_value=5)
        api_socket_conn.socket.receive = mock.Mock(return_value=b'hello')
        result_send = api_socket_conn.send(b'hello')
        result_receive = api_socket_conn.receive(5)
        self.assertEqual(result_send, 5)
        self.assertEqual(result_receive, b'hello')