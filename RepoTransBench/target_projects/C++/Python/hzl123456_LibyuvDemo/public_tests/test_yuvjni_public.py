import unittest

class YuvJniPublicTest(unittest.TestCase):
    def test_simple_arithmetic_public(self):
        x = 7
        y = 8
        self.assertEqual(x + y, 15)
        self.assertTrue(x < y + 3)
        self.assertEqual((y - x), 1)