import unittest
from src.gurugio_book.long_if import very_long_if

class TestLongIf(unittest.TestCase):
    """Tests for the very_long_if function translated from test_long_if.c"""
    
    def test_long_if_all_positive(self):
        """Test when all parameters are positive"""
        self.assertEqual(very_long_if(1, 2, 3), 1)
    
    def test_long_if_all_negative(self):
        """Test when all parameters are negative"""
        self.assertEqual(very_long_if(-1, -2, -3), -1)
    
    def test_long_if_zeros(self):
        """Test when the first parameter is zero"""
        self.assertEqual(very_long_if(0, 1, 2), 0)
    
    def test_long_if_catch_rest(self):
        """Test when parameters have mixed signs"""
        self.assertEqual(very_long_if(1, -2, 3), 99)

if __name__ == '__main__':
    unittest.main()
    print("test_long_if: OK")