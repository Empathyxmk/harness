import unittest
from siesta import auth

class DummyRequest:
    def __init__(self):
        self.headers = {}

class TestAuth(unittest.TestCase):
    def test_basic_auth(self):
        a = auth.BasicAuth('foo', 'bar')
        hdrs = a.generate_headers()
        self.assertIn('Authorization', hdrs)
        self.assertTrue(hdrs['Authorization'].startswith("Basic "))

    def test_call_sets_headers(self):
        a = auth.BasicAuth('foo', 'bar')
        req = DummyRequest()
        a.attach(req)
        self.assertIn('Authorization', req.headers)

    def test_repr(self):
        ba = auth.BasicAuth('username', 'pw')
        rep = repr(ba)
        self.assertIn('BasicAuth', rep)

    def test_bearer_token(self):
        bt = auth.BearerToken('tok123')
        hdrs = bt.generate_headers()
        self.assertEqual(hdrs['Authorization'], 'Bearer tok123')
        req = DummyRequest()
        bt.attach(req)
        self.assertIn('Authorization', req.headers)

    def test_repr_bearer(self):
        b = auth.BearerToken('tk')
        self.assertIn('BearerToken', repr(b))

    def test_api_key_header_only(self):
        ak = auth.ApiKey('mykey', 'myval', in_header=True)
        hdrs = ak.generate_headers()
        self.assertIn('mykey', hdrs)
        req = DummyRequest()
        ak.attach(req)
        self.assertIn('mykey', req.headers)

    def test_api_key_in_query_not_supported(self):
        ak = auth.ApiKey('qkey', 'qval', in_header=False)
        hdrs = ak.generate_headers()
        self.assertEqual(hdrs, {})  # Function prints msg, but no header is set

    def test_repr_api_key(self):
        ak = auth.ApiKey('api', 'value')
        self.assertIn('ApiKey', repr(ak))

if __name__ == "__main__":
    unittest.main()