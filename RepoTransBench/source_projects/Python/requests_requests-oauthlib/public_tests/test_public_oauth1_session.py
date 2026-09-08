import unittest
from requests_oauthlib import OAuth1Session

class OAuth1SessionPublicTest(unittest.TestCase):
    def setUp(self):
        self.client_key = "public_client_key"
        self.client_secret = "public_client_secret"
        self.resource_owner_key = "public_ro_key"
        self.resource_owner_secret = "public_ro_secret"

    def test_public_oauth1session_fetch_request_token_diff(self):
        session = OAuth1Session(
            self.client_key, client_secret=self.client_secret
        )
        # patch fetch_request_token for public test: use different URL and keys
        def fake_post(url, data=None, headers=None, auth=None):
            class Resp:
                status_code = 200
                def json(self_inner):
                    # response dict with changed public keys
                    return {"oauth_token": "ptok_pub1", "oauth_token_secret": "ptok_pub2"}
                @property
                def text(self_inner):
                    return "oauth_token=ptok_pub1&oauth_token_secret=ptok_pub2"
            return Resp()
        session.post = fake_post
        token = session.fetch_request_token("https://publicqa.example.com/req_token")
        self.assertEqual(token["oauth_token"], "ptok_pub1")
        self.assertEqual(token["oauth_token_secret"], "ptok_pub2")

    def test_public_oauth1session_repr_diff(self):
        sess = OAuth1Session("diff_key", client_secret="diff_secret")
        rep = repr(sess)
        self.assertIn("diff_key", rep)
        self.assertIn("OAuth1Session(", rep)