from unittest import TestCase

import routeros_api

try:
    from unittest import mock
except ImportError:
    import mock

class TestLoginRouterOsApiPublic(TestCase):
    def test_no_login_field(self):
        with self.assertRaises(Exception):
            routeros_api.RouterOsApi(None, None, None)

    def test_str_repr(self):
        session = mock.Mock()
        api = routeros_api.RouterOsApi(session, 'myuser', 'mypass')
        self.assertIn('myuser', repr(api))
        self.assertIn('myuser', str(api))