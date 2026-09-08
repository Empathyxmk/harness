import unittest
from siesta import API, foo_not_supported

class TestSiestaAPI(unittest.TestCase):
    def test_foo_not_supported_print(self):
        # Just makes sure print does not raise (for coverage)
        foo_not_supported()

    def test_api_init_and_attr(self):
        api = API("http://api.com")
        resource = api.books
        self.assertIsNotNone(resource)
        self.assertIn("/books", api.resources)
        self.assertEqual(resource.uri, "/books")
        self.assertEqual(resource.api, api)
        self.assertEqual(str(api), "<API http://api.com>")
        # __repr__ of resource
        self.assertTrue(str(resource).startswith("<Resource /books"))