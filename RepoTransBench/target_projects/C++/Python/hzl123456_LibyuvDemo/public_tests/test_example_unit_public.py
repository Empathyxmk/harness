import unittest

class ExampleUnitPublicTest(unittest.TestCase):
    def test_addition_is_correct_public(self):
        self.assertEqual(10, 5 + 5)
        self.assertEqual(-2, -1 + -1)