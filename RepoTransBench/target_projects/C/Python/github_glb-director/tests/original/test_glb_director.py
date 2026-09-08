import unittest
from src.glb_director.glb_director import add, is_palindrome, sign

class TestGlbDirector(unittest.TestCase):
    
    def test_add(self):
        # Basic, zero, negative and positive test cases
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-4, 4), 0)
        self.assertEqual(add(-7, -5), -12)
        self.assertEqual(add(100, 50), 150)
    
    def test_is_palindrome(self):
        # Palindromes and non-palindromes
        self.assertEqual(is_palindrome("madam"), 1)
        self.assertEqual(is_palindrome("racecar"), 1)
        self.assertEqual(is_palindrome("hello"), 0)
        self.assertEqual(is_palindrome("step on no pets"), 1)
        self.assertEqual(is_palindrome("abc"), 0)
        self.assertEqual(is_palindrome(""), 1)  # edge, empty string is palindrome
        self.assertEqual(is_palindrome("a"), 1)  # single character is palindrome
    
    def test_sign(self):
        self.assertEqual(sign(10), 1)
        self.assertEqual(sign(-20), -1)
        self.assertEqual(sign(0), 0)
        self.assertEqual(sign(12345), 1)
        self.assertEqual(sign(-1), -1)

if __name__ == '__main__':
    unittest.main()