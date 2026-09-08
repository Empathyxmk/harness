import unittest

class ExampleUnitPublicTest(unittest.TestCase):
    def test_multiplication_is_correct_public(self):
        self.assertEqual(9, 3 * 3)
        self.assertEqual(0, 0 * 100)