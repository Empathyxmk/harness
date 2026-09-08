import unittest
import importlib
import sys

class TestPublicInitAndSetup(unittest.TestCase):
    def test_version_number_exists_and_diff(self):
        # Ensures version exists and is a string
        from requests_oauthlib import __version__
        self.assertIsInstance(__version__, str)
        self.assertGreaterEqual(len(__version__), 5)
        # Check that version matches a typical scheme (e.g., "2.0.0"), but use different expectation
        parts = __version__.split(".")
        self.assertTrue(all(p.isdigit() for p in parts), "Version should be digits separated by dots.")

    def test_public_imports(self):
        # Check that public imports still work
        import requests_oauthlib
        self.assertTrue(hasattr(requests_oauthlib, "OAuth1"))
        self.assertTrue(hasattr(requests_oauthlib, "OAuth2"))
        self.assertTrue(hasattr(requests_oauthlib, "OAuth2Session"))

    def test_public_warning_on_old_requests(self):
        # Simulate old requests version for public, expect warning
        sys.modules.pop('requests', None) # remove cached
        import types
        old_requests = types.SimpleNamespace(__version__="1.1.0")
        sys.modules['requests'] = old_requests
        try:
            importlib.reload(importlib.import_module('requests_oauthlib'))
        except Warning as w:
            self.assertIn("You are using requests version", str(w))
        finally:
            sys.modules.pop('requests', None)
            importlib.reload(importlib.import_module('requests_oauthlib'))