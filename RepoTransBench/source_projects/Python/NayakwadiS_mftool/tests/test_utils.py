import unittest

class TestUtilsBarebone(unittest.TestCase):
    def test_basic_math(self):
        self.assertEqual(1 + 1, 2)
        self.assertTrue(isinstance([], list))

if __name__ == '__main__':
    unittest.main()