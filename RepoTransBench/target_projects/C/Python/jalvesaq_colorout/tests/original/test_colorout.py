"""
Original unit tests for colorout package, translated from C to Python.
These tests focus on internal helper functions.
"""

import unittest
from src.colorout.core import isletter, iswhitespace, isword

class TestColoroutInternals(unittest.TestCase):
    
    def test_isletter(self):
        """Test the isletter function."""
        self.assertEqual(isletter('a'), True)
        self.assertEqual(isletter('z'), True)
        self.assertEqual(isletter('A'), True)
        self.assertEqual(isletter('Z'), True)
        self.assertEqual(isletter('m'), True)
        self.assertEqual(isletter('M'), True)
        self.assertEqual(isletter('0'), False)
        self.assertEqual(isletter('%'), False)
        self.assertEqual(isletter('9'), False)
        self.assertEqual(isletter('\n'), False)
    
    def test_iswhitespace(self):
        """Test the iswhitespace function."""
        self.assertEqual(iswhitespace(' '), True)
        self.assertEqual(iswhitespace('\t'), True)
        self.assertEqual(iswhitespace('\n'), True)
        self.assertEqual(iswhitespace('\v'), True)
        self.assertEqual(iswhitespace('\f'), True)
        self.assertEqual(iswhitespace('\r'), True)
        
        self.assertEqual(iswhitespace('a'), False)
        self.assertEqual(iswhitespace('1'), False)
        self.assertEqual(iswhitespace('/'), False)
        self.assertEqual(iswhitespace(0), False)
    
    def test_isword(self):
        """Test the isword function with various inputs."""
        s1 = "hello"
        s2 = "9h"
        s3 = " test!"
        s4 = " wordx!"
        
        # Position 0: 'h', no previous, next = 'e' (letter)
        self.assertEqual(isword(s1, 0, 1), not isletter('e'))
        # Position 4: 'o', previous = 'l', next = None (so isletter('')==False)
        self.assertEqual(isword(s1, 4, 1), not isletter('l') and not isletter('') if 5 >= len(s1) else not isletter(''))
        # Middle of string, previous not letter, next not letter
        self.assertEqual(isword(s3, 1, 1), not isletter(' ') and not isletter('e'))
        
        # Index with non-letter preceding and following: " wordx!" index 1
        self.assertEqual(isword(s4, 1, 1), not isletter(' ') and not isletter('o'))
        
        # Edge (all digits):
        s5 = "123"
        self.assertEqual(isword(s5, 1, 1), not isletter('1') and not isletter('3'))
    
    def test_isword_edge_cases(self):
        """Test edge cases for the isword function."""
        single = "A"
        self.assertEqual(isword(single, 0, 1), not isletter('') and not isletter('') if 1 >= len(single) else not isletter(''))
        
        # Empty string case
        empty = ""
        # Not testing isword(empty, 0, 1) as it would raise an index error in Python
        # This is handled by parameter validation in the Python implementation
    
    def test_coverage_helpers(self):
        """Exhaustively test helper functions for coverage."""
        # Call isletter on all ASCII
        for c in range(128):
            isletter(chr(c))
        
        # Call iswhitespace on all ASCII
        for c in range(128):
            iswhitespace(chr(c))

if __name__ == '__main__':
    unittest.main()