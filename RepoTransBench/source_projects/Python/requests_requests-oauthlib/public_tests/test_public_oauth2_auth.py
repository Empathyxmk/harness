import unittest

from requests_oauthlib.oauth2_auth import OAuth2

class TestPublicOAuth2(unittest.TestCase):
    def test_public_oauth2_auth_header_diff_data(self):
        client_id = "public_client_id"
        token_data = {
            "access_token": "tok_9876543210abc",
            "token_type": "Bearer",
            "expires_in": 600,
        }
        oauth = OAuth2(client_id, token=token_data)
        class Req:
            def __init__(self):
                self.headers = {}
        req = Req()
        r2 = oauth(req)
        self.assertIn("Authorization", r2.headers)
        self.assertTrue(r2.headers["Authorization"].startswith("Bearer "))
        self.assertIn(token_data["access_token"], r2.headers["Authorization"])

    def test_public_oauth2_auth_repr_diff(self):
        oauth = OAuth2("public_id", token=None)
        rep = repr(oauth)
        self.assertIn("public_id", rep)
        self.assertTrue(rep.startswith("OAuth2("))