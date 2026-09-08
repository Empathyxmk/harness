import unittest
from siesta import API, foo_not_supported

class TestSiestaAPIPublic(unittest.TestCase):
    def test_foo_not_supported_print(self):
        # Just makes sure print does not raise (for coverage)
        foo_not_supported()

    def test_api_init_and_attr(self):
        api = API("http://publicapi.org")
        resource = api.users
        self.assertIsNotNone(resource)
        self.assertIn("/users", api.resources)
        self.assertEqual(resource.uri, "/users")
        self.assertEqual(resource.api, api)
        self.assertEqual(str(api), "<API http://publicapi.org>")
        # __repr__ of resource
        self.assertTrue(str(resource).startswith("<Resource /users"))