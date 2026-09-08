import unittest

class TestExampleUnitPublic(unittest.TestCase):
    def test_multiplication_is_correct(self):
        self.assertEqual(21, 7 * 3)