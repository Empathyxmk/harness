import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from neon_threads.sbr_testlib import sbr_mul

class TestSbrExtraPublic(unittest.TestCase):
    def test_sbr_mul_public(self):
        # Simple multiplication with different values
        self.assertEqual(sbr_mul(2, 7), 14)
        # Multiplying by zero with swapped operands
        self.assertEqual(sbr_mul(0, 11), 0)
        # Multiplying negatives with different values
        self.assertEqual(sbr_mul(-3, -5), 15)
        self.assertEqual(sbr_mul(-4, 3), -12)
        # Commutativity with different values
        self.assertEqual(sbr_mul(9, 2), sbr_mul(2, 9))

if __name__ == '__main__':
    unittest.main()
    print("All sbr_mul PUBLIC tests passed.")