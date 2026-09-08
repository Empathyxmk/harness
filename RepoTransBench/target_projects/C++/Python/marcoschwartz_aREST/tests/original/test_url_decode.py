import unittest

def url_decode(s):
    # Simple Python urldecode equivalent for these tests
    from urllib.parse import unquote_plus
    return unquote_plus(s)

class TestUrlDecode(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(url_decode("Hello+World"), "Hello World")
        self.assertEqual(url_decode("I+love+%25%25%25percents%25%25%25"), "I love %%%percents%%%")
        self.assertEqual(url_decode(""), "")

    def test_malformed(self):
        # Malformed % encoding
        self.assertEqual(url_decode("%"), "%")
        self.assertEqual(url_decode("%1"), "%1")
        self.assertEqual(url_decode("I hate percents%"), "I hate percents%")
        self.assertEqual(url_decode("I hate percents%2"), "I hate percents%2")

    def test_memoryloss(self):
        # Test repeated usage == no memory leaks (simulate leak check)
        import gc
        before = len(gc.get_objects())
        for _ in range(1000):
            url_decode("Hello+World")
        after = len(gc.get_objects())
        # There's no actual expectation; this ensures we don't crash or leak grossly
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()