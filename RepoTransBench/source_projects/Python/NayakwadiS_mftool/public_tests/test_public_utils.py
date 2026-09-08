import unittest

class TestUtilsBarebonePublic(unittest.TestCase):
    def test_basic_math_public(self):
        self.assertEqual(2 * 3, 6)
        self.assertTrue(isinstance({}, dict))

if __name__ == '__main__':
    unittest.main()