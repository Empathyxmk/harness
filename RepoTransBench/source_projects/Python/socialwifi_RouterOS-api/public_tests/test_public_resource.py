from unittest import TestCase

from routeros_api import resource
from routeros_api import query

try:
    from unittest import mock
except ImportError:
    import mock

class TestResourcePublic(TestCase):
    def test_get_collection_with_arguments(self):
        sentence = mock.Mock()
        connection = mock.Mock()
        res = resource.Resource(connection, b'/interface')
        sentence.side_effect = None
        connection.communicator.call().get.return_value = [
            {b"name": b"eth10"}, {b"name": b"eth20"}
        ]
        connection.communicator.call.return_value.get = connection.communicator.call().get
        result = res.get(name="eth10")
        self.assertEqual(result, [{b"name": b"eth10"}, {b"name": b"eth20"}])

    def test_set_works(self):
        connection = mock.Mock()
        resource_obj = resource.Resource(connection, b'/ip/firewall')
        resource_obj.set(id=2, action="accept", chain="forward")
        connection.communicator.call.assert_called_with(
            b'/ip/firewall', 'set', {'id': 2, 'action': 'accept', 'chain': 'forward'}
        )

    def test_remove_works(self):
        connection = mock.Mock()
        resource_obj = resource.Resource(connection, b'/ip/hotspot')
        resource_obj.remove(id=9)
        connection.communicator.call.assert_called_with(
            b'/ip/hotspot', 'remove', {'id': 9}
        )

    def test_find_returns_results(self):
        connection = mock.Mock()
        resource_obj = resource.Resource(connection, b'/ip/address')
        connection.communicator.call().get.return_value = [{b"name": b"address1"}]
        connection.communicator.call.return_value.get = connection.communicator.call().get
        result = resource_obj.find(address="192.168.2.1")
        self.assertEqual(result, [{b"name": b"address1"}])

    def test_query_is_called(self):
        connection = mock.Mock()
        res = resource.Resource(connection, b'/routing/ospf')
        q = query.Query()
        res.filter(id=22)
        res.filter(area="backbone")
        res.get(comment="testing", query=q)
        connection.communicator.call.assert_any_call(
            b'/routing/ospf', 'print', {'comment': 'testing'}, q
        )