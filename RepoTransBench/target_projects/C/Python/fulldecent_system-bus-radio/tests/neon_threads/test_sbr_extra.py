import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from neon_threads.sbr_testlib import sbr_mul

class TestSbrExtra(unittest.TestCase):
    def test_sbr_mul(self):
        # Simple multiplication
        self.assertEqual(sbr_mul(3, 4), 12)
        # Multiplying by zero
        self.assertEqual(sbr_mul(7, 0), 0)
        # Multiplying negatives
        self.assertEqual(sbr_mul(-2, -4), 8)
        self.assertEqual(sbr_mul(-2, 4), -8)
        # Commutativity
        self.assertEqual(sbr_mul(5, 6), sbr_mul(6, 5))

if __name__ == '__main__':
    unittest.main()
    print("All sbr_mul tests passed.")