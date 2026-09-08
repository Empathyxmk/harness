import unittest
from urllib.parse import unquote_plus

class DummyArestPublic:
    def __init__(self):
        self._ver = "3.0.3"
        self._id = ""
        self._name = ""
        self._api_key = ""

    def version(self):
        return self._ver
    def set_id(self, s):
        self._id = "" if s is None else s
    def id(self):
        return self._id

    def set_name(self, s):
        self._name = "" if s is None else s
    def name(self):
        return self._name

    def set_api_key(self, s):
        self._api_key = "" if s is None else s
    def api_key(self):
        return self._api_key

    def url_decode(self, encoded):
        return unquote_plus(encoded)

class TestARESTBasicPublic(unittest.TestCase):
    def setUp(self):
        self.arest = DummyArestPublic()

    def test_version(self):
        self.assertEqual(self.arest.version(), "3.0.3")

    def test_id(self):
        self.arest.set_id("node_public_123")
        self.assertEqual(self.arest.id(), "node_public_123")

    def test_name(self):
        self.arest.set_name("PublicDevice")
        self.assertEqual(self.arest.name(), "PublicDevice")

    def test_api_key(self):
        self.arest.set_api_key("pubSECRETKEY")
        self.assertEqual(self.arest.api_key(), "pubSECRETKEY")

    def test_url_decode(self):
        encoded = "public%20url%21"
        decoded = self.arest.url_decode(encoded)
        self.assertEqual(decoded, "public url!")

    def test_default_constructor(self):
        ar = DummyArestPublic()
        self.assertEqual(ar.id(), "")
        self.assertEqual(ar.name(), "")
        self.assertEqual(ar.api_key(), "")

    def test_set_id_null(self):
        ar = DummyArestPublic()
        ar.set_id(None)
        self.assertEqual(ar.id(), "")

    def test_set_name_null(self):
        ar = DummyArestPublic()
        ar.set_name(None)
        self.assertEqual(ar.name(), "")

    def test_set_api_key_null(self):
        ar = DummyArestPublic()
        ar.set_api_key(None)
        self.assertEqual(ar.api_key(), "")

if __name__ == '__main__':
    unittest.main()