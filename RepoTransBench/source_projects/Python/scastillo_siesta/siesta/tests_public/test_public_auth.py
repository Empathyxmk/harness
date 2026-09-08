import unittest
from siesta import auth

class DummyRequestPublic:
    def __init__(self):
        self.headers = {}

class TestAuthPublic(unittest.TestCase):
    def test_basic_auth(self):
        a = auth.BasicAuth('alice', 'wonderland')
        hdrs = a.generate_headers()
        self.assertIn('Authorization', hdrs)
        self.assertTrue(hdrs['Authorization'].startswith("Basic "))

    def test_call_sets_headers(self):
        a = auth.BasicAuth('alice', 'wonderland')
        req = DummyRequestPublic()
        a.attach(req)
        self.assertIn('Authorization', req.headers)

    def test_repr(self):
        ba = auth.BasicAuth('someone', 'secret')
        rep = repr(ba)
        self.assertIn('BasicAuth', rep)

    def test_bearer_token(self):
        bt = auth.BearerToken('publictoken456')
        hdrs = bt.generate_headers()
        self.assertEqual(hdrs['Authorization'], 'Bearer publictoken456')
        req = DummyRequestPublic()
        bt.attach(req)
        self.assertIn('Authorization', req.headers)

    def test_repr_bearer(self):
        b = auth.BearerToken('pubtoken')
        self.assertIn('BearerToken', repr(b))

    def test_api_key_header_only(self):
        ak = auth.ApiKey('pubkey', 'pubval', in_header=True)
        hdrs = ak.generate_headers()
        self.assertIn('pubkey', hdrs)
        req = DummyRequestPublic()
        ak.attach(req)
        self.assertIn('pubkey', req.headers)

    def test_api_key_in_query_not_supported(self):
        ak = auth.ApiKey('querykey', 'queryval', in_header=False)
        hdrs = ak.generate_headers()
        self.assertEqual(hdrs, {})  # Function prints msg, but no header is set

    def test_repr_api_key(self):
        ak = auth.ApiKey('pubapi', 'pubvalue')
        self.assertIn('ApiKey', repr(ak))

if __name__ == "__main__":
    unittest.main()