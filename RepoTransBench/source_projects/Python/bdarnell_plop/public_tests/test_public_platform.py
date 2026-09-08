import unittest
from plop import platform

class PublicPlatformTest(unittest.TestCase):
    def test_get_hostname(self):
        h = platform.get_hostname()
        self.assertIsInstance(h, str)
        self.assertTrue(len(h) >= 0)

    def test_get_username(self):
        u = platform.get_username()
        self.assertIsInstance(u, str)
        self.assertTrue(len(u) >= 0)