import unittest

def publicCompare(a, b):
    if a == b:
        return 0
    elif a < b:
        return -1
    else:
        return 1

class ComparePublicTest(unittest.TestCase):
    def test_compare_different_numbers_public(self):
        self.assertEqual(publicCompare(5,5), 0)
        self.assertEqual(publicCompare(2,10), -1)
        self.assertEqual(publicCompare(77,33), 1)