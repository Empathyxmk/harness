import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from neon_threads.sbr_testlib import sbr_mul

class TestSbr(unittest.TestCase):
    def test_mul_basic(self):
        self.assertEqual(sbr_mul(2, 3), 6)
        self.assertEqual(sbr_mul(0, 10), 0)
        self.assertEqual(sbr_mul(-2, 3), -6)
    
    def test_mul_one(self):
        self.assertEqual(sbr_mul(1, 999), 999)
        self.assertEqual(sbr_mul(-1, 7), -7)

if __name__ == '__main__':
    unittest.main()