from unittest import TestCase

try:
    from unittest import mock
except ImportError:
    import mock

from routeros_api import api_communicator
from routeros_api import exceptions


class TestCommunicatorPublic(TestCase):
    def test_login_call(self):
        base = mock.Mock()
        base.receive_sentence.return_value = [b'!done', b'=ret=another-hex',
                                              b'.tag=99']
        communicator = api_communicator.ApiCommunicator(base)
        response = communicator.call('/test', 'login').get()
        self.assertEqual(response.done_message['ret'], b'another-hex')

    def test_normal_call(self):
        base = mock.Mock()
        base.receive_sentence.side_effect = [[b'!re', b'=p=q', b'.tag=3'],
                                             [b'!done', b'.tag=3']]
        communicator = api_communicator.ApiCommunicator(base)
        response = communicator.call('/routing/', 'print').get()
        self.assertEqual(response, [{'p': b'q'}])

    def test_mixed_calls(self):
        base = mock.Mock()
        base.receive_sentence.side_effect = [[b'!re', b'=a1=b1', b'.tag=42'],
                                             [b'!re', b'=a2=b2', b'.tag=43'],
                                             [b'!done', b'.tag=42'],
                                             [b'!done', b'.tag=43']]
        communicator = api_communicator.ApiCommunicator(base)
        promise = communicator.call('/ip/firewall/', 'print')
        response2 = communicator.call('/ip/firewall/', 'print').get()
        response1 = promise.get()
        self.assertEqual(response1, [{'a1': b'b1'}])
        self.assertEqual(response2, [{'a2': b'b2'}])

    def test_error_call(self):
        base = mock.Mock()
        base.receive_sentence.side_effect = [[b'!trap', b'=message=z',
                                              b'.tag=2'],
                                             [b'!done', b'.tag=2']]
        communicator = api_communicator.ApiCommunicator(base)
        promise = communicator.call('/ip/address/', 'print')
        self.assertRaises(exceptions.RouterOsApiCommunicationError,
                          promise.get)

    def test_empty_call(self):
        base = mock.Mock()
        base.receive_sentence.side_effect = [[b'!empty', b'.tag=8'],
                                             [b'!done', b'.tag=8']]
        communicator = api_communicator.ApiCommunicator(base)
        response = communicator.call('/system/resource/', 'print').get()
        self.assertEqual(response, [])

    def test_query_call(self):
        base = mock.Mock()
        base.receive_sentence.return_value = [b'!done', b'.tag=5']
        communicator = api_communicator.ApiCommunicator(base)
        communicator.call('/routing/', 'print', queries={'foo': 'bar'}).get()
        base.send_sentence.assert_called_once_with(
            [b'/routing/print', b'?foo=bar', b'.tag=1'])

    def test_set_call(self):
        base = mock.Mock()
        base.receive_sentence.return_value = [b'!done', b'.tag=11']
        communicator = api_communicator.ApiCommunicator(base)
        communicator.call('/routing/', 'set', {'foo': b'bar'})
        base.send_sentence.assert_called_once_with(
            [b'/routing/set', b'=foo=bar', b'.tag=1'])

    def test_call_with_arguments(self):
        base = mock.Mock()
        base.receive_sentence.return_value = [b'!done', b'.tag=16']
        communicator = api_communicator.ApiCommunicator(base)
        communicator.call('/system/monitor-traffic/', 'monitor', {'device': 'eth10'})
        base.send_sentence.assert_called_once_with(
            [b'/system/monitor-traffic/monitor', b'=device=eth10', b'.tag=1'])

    def test_call_without_arguments(self):
        base = mock.Mock()
        base.receive_sentence.return_value = [b'!done', b'.tag=22']
        communicator = api_communicator.ApiCommunicator(base)
        communicator.call('/system/monitor-traffic/', 'monitor', {'count': None})
        base.send_sentence.assert_called_once_with(
            [b'/system/monitor-traffic/monitor', b'=count', b'.tag=1'])

    def test_async_error_raises_when_synchronizing(self):
        base = mock.Mock()
        base.receive_sentence.side_effect = [
            [b'!trap', b'=message=test', b'.tag=5'],
            [b'!done', b'.tag=6'],
            [b'!done', b'.tag=5']]
        communicator = api_communicator.ApiCommunicator(base)
        promise = communicator.call('/ip/firewall/', 'print')
        communicator.call('/ip/firewall/', 'print').get()
        self.assertRaises(exceptions.RouterOsApiCommunicationError,
                          promise.get)