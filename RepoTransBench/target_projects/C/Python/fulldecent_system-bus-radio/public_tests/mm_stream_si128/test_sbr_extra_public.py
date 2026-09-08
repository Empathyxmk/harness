import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from mm_stream_si128.sbr_testlib import sbr_add

class TestSbrExtraPublic(unittest.TestCase):
    def test_sbr_add_public(self):
        # Simple addition with different values
        self.assertEqual(sbr_add(10, 5), 15)
        # Negative numbers with different values
        self.assertEqual(sbr_add(-7, -2), -9)
        # Addition with zero, swapped order
        self.assertEqual(sbr_add(0, 12), 12)
        # Commutativity with different values
        self.assertEqual(sbr_add(8, 3), sbr_add(3, 8))

if __name__ == '__main__':
    unittest.main()
    print("All sbr_add PUBLIC tests passed.")