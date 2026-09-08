import unittest

# Import from the package directly since sys.path manipulation can cause trouble for pytest
from requests_oauthlib.core import set_token

class DummySession:
    def __init__(self):
        self.token = None

class PublicCoreTest(unittest.TestCase):
    def test_set_token_public_diff_token(self):
        sess = DummySession()
        set_token(sess, {"access_token": "unicorn_xyz", "token_type": "Bearer"})
        self.assertIsInstance(sess.token, dict)
        self.assertIn("access_token", sess.token)
        self.assertEqual(sess.token["access_token"], "unicorn_xyz")

    def test_set_token_public_other_diff(self):
        sess = DummySession()
        set_token(sess, {"access_token": "golden_public_token", "token_type": "macaroons"})
        self.assertIsNotNone(sess.token)
        self.assertEqual(sess.token["access_token"], "golden_public_token")