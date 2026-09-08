"""Test for test_test2() with empty string."""
import unittest
from src.php_test import test_test2

class Test011Test2Empty(unittest.TestCase):
    """Test case for test_test2() with empty string."""
    
    def test_test2_empty(self):
        """Test that test_test2("") returns "Hello "."""
        result = test_test2("")
        self.assertEqual(result, "Hello ")
        # PHP var_dump would show string length, we'll assert that too
        self.assertEqual(len(result), 6)