import unittest

class TestMFInitMinimalPublic(unittest.TestCase):
    def test_dummy_value_public(self):
        self.assertFalse("DUMMY".islower())

if __name__ == '__main__':
    unittest.main()