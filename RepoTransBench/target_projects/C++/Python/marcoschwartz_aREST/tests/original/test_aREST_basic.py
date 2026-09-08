import unittest
from urllib.parse import unquote_plus

class DummyArest:
    def __init__(self):
        self._ver = "2.9.7"
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
    def device(self):
        return self._name

    def set_api_key(self, s):
        self._api_key = "" if s is None else s
    def get_api_key(self):
        return self._api_key

    def url_decode(self, encoded):
        # In-place decode, modeled similar to C++ char* mutability
        s = encoded
        decoded = unquote_plus(s)
        # If encoded is a list or mutable buffer, update in-place
        if isinstance(encoded, list):
            encoded.clear()
            encoded += list(decoded)
        return decoded

class TestARESTBasic(unittest.TestCase):
    def setUp(self):
        self.arest = DummyArest()

    def test_version(self):
        self.assertEqual(self.arest.version(), "2.9.7")

    def test_id(self):
        self.arest.set_id("123456")
        self.assertEqual(self.arest.id(), "123456")

    def test_name(self):
        self.arest.set_name("TestDevice")
        self.assertEqual(self.arest.device(), "TestDevice")

    def test_api_key(self):
        self.arest.set_api_key("APIKEY")
        self.assertEqual(self.arest.get_api_key(), "APIKEY")

    def test_url_decode(self):
        test = list("hello%20world%21")
        # encoded is a list for mutability
        decoded = self.arest.url_decode("".join(test))
        self.assertEqual(decoded, "hello world!")
        test2 = list("no_encoding")
        decoded2 = self.arest.url_decode("".join(test2))
        self.assertEqual(decoded2, "no_encoding")

    def test_default_constructor(self):
        ar = DummyArest()
        self.assertEqual(ar.version(), "2.9.7")
        self.assertEqual(ar.id(), "")
        self.assertEqual(ar.device(), "")

    def test_set_id_null(self):
        ar = DummyArest()
        ar.set_id(None)
        self.assertEqual(ar.id(), "")

    def test_set_name_null(self):
        ar = DummyArest()
        ar.set_name(None)
        self.assertEqual(ar.device(), "")

    def test_set_api_key_null(self):
        ar = DummyArest()
        ar.set_api_key(None)
        self.assertEqual(ar.get_api_key(), "")

if __name__ == "__main__":
    unittest.main()