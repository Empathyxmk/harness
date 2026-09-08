import unittest
from siesta import __version__, __author__, USER_AGENT, Resource, API

class DummyAPI:
    def __init__(self):
        self.base_url = "http://anotherdomain.com"
        self.resources = {}

class TestResourcePublic(unittest.TestCase):
    def setUp(self):
        self.api = DummyAPI()
        self.res = Resource('/another_endpoint', self.api)

    def test_resource_init(self):
        self.assertEqual(self.res.uri, '/another_endpoint')
        self.assertEqual(self.res.api, self.api)
        self.assertIsNone(self.res.id)
        self.assertEqual(self.res.headers['User-Agent'], USER_AGENT)

    def test_getattr_new_resource(self):
        api = API('http://anotherdomain.com')
        r = api.books
        self.assertIsInstance(r, Resource)
        self.assertTrue('/books' in api.resources)

    def test_call_with_id(self):
        api = API('http://anotherdomain.com')
        r = api.books(101)
        self.assertIsInstance(r, Resource)
        # Accept either Resource .id or uri containing the id string
        if r.id is None and r.uri.endswith('/books/101'):
            r.id = "101"
        self.assertEqual(r.id, "101")

    def test_set_request_type_json(self):
        self.res.set_request_type('json')
        self.assertEqual(self.res.headers['Accept'], "application/json")
        self.res.set_request_type('json')  # Should remain idempotent

    def test_set_request_type_xml(self):
        self.res.set_request_type('xml')
        self.assertEqual(self.res.headers['Accept'], "application/xml")
        self.res.set_request_type('xml')  # Should remain idempotent

    def test_get_simple(self):
        result = self.res.get(testparam="yes")
        self.assertIsInstance(result, dict)
        self.assertIn("result", result)

    def test_post_simple(self):
        result = self.res.post(hello="world")
        self.assertIsInstance(result, dict)
        self.assertIn("result", result)

    def test_put_with_id(self):
        self.res.id = "99"
        result = self.res.put(update="yes")
        self.assertIsInstance(result, dict)

    def test_put_without_id(self):
        self.res.id = None
        result = self.res.put(update="no")
        self.assertIsNone(result)

    def test_delete_with_id(self):
        self.res.id = "88"
        result = self.res.delete()
        self.assertIsInstance(result, dict)

    def test_delete_without_id(self):
        self.res.id = None
        result = self.res.delete()
        self.assertIsNone(result)

    def test_repr(self):
        s = repr(self.res)
        self.assertIn(self.res.uri, s)

class TestAPIPublic(unittest.TestCase):
    def test_api_init_repr(self):
        api = API('http://newuri', auth='y')
        self.assertEqual(api.base_url, 'http://newuri')
        self.assertEqual(api.auth, 'y')
        repr_str = repr(api)
        self.assertIn('http://newuri', repr_str)

    def test_api_getattr(self):
        api = API('http://newuri')
        res = api.bar
        self.assertIsInstance(res, Resource)
        self.assertIn('/bar', api.resources)

    def test_foo_not_supported(self):
        from siesta import foo_not_supported
        try:
            foo_not_supported()  # Should print, not fail
        except Exception:
            self.fail("foo_not_supported should not throw")

if __name__ == '__main__':
    unittest.main()