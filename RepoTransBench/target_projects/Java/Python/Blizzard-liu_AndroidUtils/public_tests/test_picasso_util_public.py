import unittest

class TestPicassoUtilPublic(unittest.TestCase):
    def test_url_is_jpeg_public(self):
        url = "https://example.org/altpic.jpeg"
        self.assertTrue(url.endswith('.jpeg'))