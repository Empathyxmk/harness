"""
Public unit tests for colorout package, translated from C to Python.
These tests focus on public API functions.
"""

import unittest
from src.colorout.core import is_word, is_string_number

class TestColoroutPublic(unittest.TestCase):
    
    def test_isword_public_fn(self):
        """Test the is_word function with public test cases."""
        self.assertEqual(is_word("hello123"), True)
        self.assertEqual(is_word("_alpha"), True)
        self.assertEqual(is_word("..beta"), True)
        # Change: use symbols as non-words
        self.assertEqual(is_word("?h"), False)
        self.assertEqual(is_word("!@#"), False)
    
    def test_isword_edge_cases_public_fn(self):
        """Test edge cases for the is_word function."""
        self.assertEqual(is_word("1234"), False)        # all digit
        self.assertEqual(is_word("_"), True)            # single underscore
        self.assertEqual(is_word("."), True)            # single dot
        self.assertEqual(is_word("6e4"), False)         # "6e4" not treated as word (digit start)
    
    def test_isstringnumber_public_fn(self):
        """Test the is_string_number function."""
        self.assertEqual(is_string_number("12345"), True)    # simple integer
        self.assertEqual(is_string_number("-9876"), True)    # negative
        self.assertEqual(is_string_number("+555"), True)     # positive sign
        self.assertEqual(is_string_number("007"), True)      # leading zeros
        self.assertEqual(is_string_number("12a34"), False)   # alpha inside
        self.assertEqual(is_string_number("abc"), False)     # not a number
    
    def test_isstringnumber_edge_cases_public_fn(self):
        """Test edge cases for the is_string_number function."""
        self.assertEqual(is_string_number(""), False)          # empty string
        self.assertEqual(is_string_number("+"), False)         # just sign, no digits
        self.assertEqual(is_string_number("-"), False)         # just sign, no digits
        self.assertEqual(is_string_number("--100"), False)     # double sign, invalid
        self.assertEqual(is_string_number("9-3"), False)       # sign in wrong place

if __name__ == '__main__':
    unittest.main()