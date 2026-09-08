import unittest

class TestExampleUnitAppPublic(unittest.TestCase):
    def test_multiplication_is_correct_public(self):
        self.assertEqual(15, 3 * 5)