import json
import time
from unittest import TestCase, mock
from oauthlib.oauth2 import TokenExpiredError, OAuth2Error
from oauthlib.oauth2 import MismatchingStateError
from oauthlib.oauth2 import WebApplicationClient, MobileApplicationClient
from oauthlib.oauth2 import LegacyApplicationClient, BackendApplicationClient
from requests_oauthlib import OAuth2Session, TokenUpdated
import requests
from base64 import b64encode

PUBLIC_CODE = "pubcde234ser"
public_fake_time = time.time()

def public_fake_token(token):
    def fake_send(r, **kwargs):
        resp = mock.MagicMock()
        resp.text = json.dumps(token)
        return resp
    return fake_send

class OAuth2SessionPublicTest(TestCase):
    def setUp(self):
        self.token = {
            "token_type": "Bearer",
            "access_token": "pubtok123456789",
            "refresh_token": "pubrtok987654321",
            "expires_in": 1234,
            "expires_at": public_fake_time + 1234,
        }
        self.pub_client_id = "publicclientid"
        self.pub_client_secret = "publicclientsecret"
        self.client_WebApplication = WebApplicationClient(self.pub_client_id, code=PUBLIC_CODE)
        self.client_LegacyApplication = LegacyApplicationClient(self.pub_client_id)
        self.client_BackendApplication = BackendApplicationClient(self.pub_client_id)
        self.client_MobileApplication = MobileApplicationClient(self.pub_client_id)
        self.clients = [
            self.client_WebApplication,
            self.client_LegacyApplication,
            self.client_BackendApplication,
        ]
        self.all_clients = self.clients + [self.client_MobileApplication]

    def test_add_token_public(self):
        token = "Bearer " + self.token["access_token"]
        def verifier(r, **kwargs):
            auth_header = r.headers.get(str("Authorization"), None)
            self.assertEqual(auth_header, token)
            resp = mock.MagicMock()
            resp.cookies = []
            return resp
        for client in self.all_clients:
            sess = OAuth2Session(client=client, token=self.token)
            sess.send = verifier
            sess.get("https://public.example.com/test")

    def test_authorization_url_public(self):
        url = "https://public.example.com/authenticate?pubfoo=bar"
        web = WebApplicationClient(self.pub_client_id)
        s = OAuth2Session(client=web)
        auth_url, state = s.authorization_url(url)
        self.assertIn(state, auth_url)
        self.assertIn(self.pub_client_id, auth_url)
        self.assertIn("response_type=code", auth_url)

        mobile = MobileApplicationClient(self.pub_client_id)
        s = OAuth2Session(client=mobile)
        auth_url, state = s.authorization_url(url)
        self.assertIn(state, auth_url)
        self.assertIn(self.pub_client_id, auth_url)
        self.assertIn("response_type=token", auth_url)

    def test_pkce_authorization_url_public(self):
        url = "https://public.example.com/authenticate?pubfoo=bar"
        web = WebApplicationClient(self.pub_client_id)
        s = OAuth2Session(client=web, pkce="plain")
        auth_url, state = s.authorization_url(url)
        self.assertIn(state, auth_url)
        self.assertIn(self.pub_client_id, auth_url)
        self.assertIn("response_type=code", auth_url)
        self.assertIn("code_challenge=", auth_url)
        self.assertIn("code_challenge_method=plain", auth_url)

        mobile = MobileApplicationClient(self.pub_client_id)
        s = OAuth2Session(client=mobile, pkce="plain")
        auth_url, state = s.authorization_url(url)
        self.assertIn(state, auth_url)
        self.assertIn(self.pub_client_id, auth_url)
        self.assertIn("response_type=token", auth_url)
        self.assertIn("code_challenge=", auth_url)
        self.assertIn("code_challenge_method=plain", auth_url)

    @mock.patch("time.time", new=lambda: public_fake_time)
    def test_refresh_token_request_public(self):
        self.expired_token = dict(self.token)
        self.expired_token["expires_in"] = "-20"
        del self.expired_token["expires_at"]

        def fake_refresh(r, **kwargs):
            if "/refresh" in r.url:
                self.assertNotIn("Authorization", r.headers)
            resp = mock.MagicMock()
            resp.text = json.dumps(self.token)
            return resp

        for client in self.clients:
            sess = OAuth2Session(client=client, token=self.expired_token)
            self.assertRaises(TokenExpiredError, sess.get, "https://public.example.com/t")

        for client in self.clients:
            sess = OAuth2Session(client=client, token=self.expired_token, auto_refresh_url="https://public.example.com/refresh")
            sess.send = fake_refresh
            self.assertRaises(TokenUpdated, sess.get, "https://public.example.com/t")

        def token_updater(token):
            self.assertEqual(token, self.token)

        for client in self.clients:
            sess = OAuth2Session(
                client=client,
                token=self.expired_token,
                auto_refresh_url="https://public.example.com/refresh",
                token_updater=token_updater,
            )
            sess.send = fake_refresh
            sess.get("https://public.example.com/t")