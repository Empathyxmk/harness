from unittest import TestCase

from routeros_api import exceptions

try:
    from unittest import mock
except ImportError:
    import mock

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    import io
    BytesIO = io.BytesIO

from routeros_api import base_api


class TestEncodeLengthPublic(TestCase):
    def test_two(self):
        result = base_api._encode_length(2)
        expected_number = 2
        expected_length = 1
        expected = (expected_number, expected_length)
        self.assertEqual(expected, result)

    def test_seven(self):
        result = base_api._encode_length(7)
        expected_number = 7
        expected_length = 1
        expected = (expected_number, expected_length)
        self.assertEqual(expected, result)

    def test_over_0x80(self):
        result = base_api._encode_length(400)
        expected_number = 33168
        expected_length = 2
        expected = (expected_number, expected_length)
        self.assertEqual(expected, result)

    def test_over_0x3FFF(self):
        result = base_api._encode_length(20000)
        expected_number = 12997584
        expected_length = 3
        expected = (expected_number, expected_length)
        self.assertEqual(expected, result)

    def test_biggest(self):
        result = base_api._encode_length(0x1FFFFFFF)
        expected_number = 0xF1FFFFFFF
        expected_length = 5
        expected = (expected_number, expected_length)
        self.assertEqual(expected, result)

    def test_too_big_fails(self):
        self.assertRaises(exceptions.FatalRouterOsApiError,
                          base_api._encode_length, 0x1FFFFFFFF)


class TestDecodeLengthPublic(TestCase):
    def test_seven(self):
        data = BytesIO(b"\x07")
        self.assertEqual(7, base_api.decode_length(data.read))

    def test_over_0x80(self):
        data = BytesIO(b"\x82\x90")
        self.assertEqual(400, base_api.decode_length(data.read))

    def test_over_0x3FFF(self):
        data = BytesIO(b"\xc4\xe6\x10")
        self.assertEqual(20000, base_api.decode_length(data.read))

    def test_biggest(self):
        data = BytesIO(b"\xF1\xFF\xFF\xFF\xFF")
        self.assertEqual(0x1FFFFFFF, base_api.decode_length(data.read))

    def test_invalid_prefix(self):
        data = BytesIO(b"\xFA")
        self.assertRaises(exceptions.FatalRouterOsApiError,
                          base_api.decode_length, data.read)


class TestToBytesPublic(TestCase):
    def test_seven(self):
        result = base_api.to_bytes(7, 1)
        expected = b'\x07'
        self.assertEqual(expected, result)

    def test_multiple_bytes(self):
        result = base_api.to_bytes(0x2223, 2)
        expected = b'\x22\x23'
        self.assertEqual(expected, result)


class TestConnectionPublic(TestCase):
    def test_sending(self):
        socket = mock.Mock()
        connection = base_api.Connection(socket)
        connection.send_sentence([b'baz', b'qux'])
        expected = [
            mock.call(b'\x03baz'),
            mock.call(b'\x03qux'),
            mock.call(b'\x00'),
        ]
        self.assertEqual(expected, socket.send.mock_calls)

    def test_receiving(self):
        socket = mock.Mock()
        socket.receive.side_effect = [b'\x04', b'test', b'\x04', b'case',
                                      b'\x00']
        connection = base_api.Connection(socket)
        result = connection.receive_sentence()
        self.assertEqual([b'test', b'case'], result)
        expected = [
            mock.call(1),
            mock.call(4),
            mock.call(1),
            mock.call(4),
            mock.call(1),
        ]
        self.assertEqual(expected, socket.receive.mock_calls)