import unittest
from secure import (
    ContentSecurityPolicy,
    CustomHeader,
    Preset,
    Secure,
    Server,
    StrictTransportSecurity,
)

class PublicMockResponse:
    def __init__(self):
        self.headers: dict[str, str] = {}

    def set_header(self, key: str, value: str):
        self.headers[key] = value

class PublicMockResponseWithSetHeader:
    def __init__(self):
        self.headers: dict[str, str] = {}
        self.storage: dict[str, str] = {}

    def set_header(self, key: str, value: str):
        self.storage[key] = value

class TestSecurePublic(unittest.TestCase):
    def setUp(self):
        self.secure = Secure(
            custom=[
                CustomHeader("X-Public-Header-1", "PubValue1"),
                CustomHeader("X-Public-Header-2", "PubValue2"),
            ]
        )
        self.secure.headers = {
            header.header_name: header.header_value
            for header in self.secure.headers_list
        }

    def test_with_public_headers(self):
        secure_headers = Secure(
            cache=None,
            csp=ContentSecurityPolicy().default_src("'self'").img_src("'public'"),
            coop=None,
            hsts=None,
            permissions=None,
            referrer=None,
            server=Server().set("PublicServer"),
            custom=[CustomHeader("X-Test-Key", "TestVal")],
            xcto=None,
            xfo=None,
        )
        response = PublicMockResponse()
        secure_headers.set_headers(response)
        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(
            response.headers["Content-Security-Policy"],
            "default-src 'self'; img-src 'public'"
        )
        self.assertIn("Server", response.headers)
        self.assertEqual(response.headers["Server"], "PublicServer")
        self.assertIn("X-Test-Key", response.headers)
        self.assertEqual(response.headers["X-Test-Key"], "TestVal")
        self.assertNotIn("Strict-Transport-Security", response.headers)

    def test_from_preset_basic_public(self):
        secure_headers = Secure.from_preset(Preset.BASIC)
        response = PublicMockResponse()

        secure_headers.set_headers(response)
        self.assertIn("Cache-Control", response.headers)
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertIn("Referrer-Policy", response.headers)
        self.assertEqual(
            response.headers["Referrer-Policy"], "strict-origin-when-cross-origin"
        )
        self.assertIn("Server", response.headers)
        self.assertEqual(response.headers["Server"], "")
        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"], "max-age=31536000"
        )
        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("X-Frame-Options", response.headers)
        self.assertEqual(response.headers["X-Frame-Options"], "SAMEORIGIN")
        self.assertNotIn("Content-Security-Policy", response.headers)
        self.assertNotIn("Permissions-Policy", response.headers)
        self.assertNotIn("Cross-Origin-Opener-Policy", response.headers)

    def test_from_preset_strict_public(self):
        secure_headers = Secure.from_preset(Preset.STRICT)
        response = PublicMockResponse()

        secure_headers.set_headers(response)
        self.assertIn("Cache-Control", response.headers)
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(
            response.headers["Content-Security-Policy"],
            (
                "default-src 'self'; script-src 'self'; style-src 'self'; "
                "object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
            ),
        )
        self.assertIn("Cross-Origin-Embedder-Policy", response.headers)
        self.assertEqual(
            response.headers["Cross-Origin-Embedder-Policy"], "require-corp"
        )
        self.assertIn("Cross-Origin-Opener-Policy", response.headers)
        self.assertEqual(response.headers["Cross-Origin-Opener-Policy"], "same-origin")
        self.assertIn("Permissions-Policy", response.headers)
        self.assertEqual(
            response.headers["Permissions-Policy"],
            "geolocation=(), microphone=(), camera=()",
        )
        self.assertIn("Referrer-Policy", response.headers)
        self.assertEqual(response.headers["Referrer-Policy"], "no-referrer")
        self.assertIn("Server", response.headers)
        self.assertEqual(response.headers["Server"], "")
        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"],
            "max-age=63072000; includeSubDomains; preload",
        )
        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("X-Frame-Options", response.headers)
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")

    def test_custom_headers_public(self):
        custom_server = Server().set("AnotherServer")
        custom_csp = ContentSecurityPolicy().default_src("'public'").style_src("'test'")

        secure_headers = Secure(server=custom_server, csp=custom_csp)
        response = PublicMockResponse()

        secure_headers.set_headers(response)

        self.assertIn("Server", response.headers)
        self.assertEqual(response.headers["Server"], "AnotherServer")

        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(
            response.headers["Content-Security-Policy"],
            "default-src 'public'; style-src 'test'",
        )