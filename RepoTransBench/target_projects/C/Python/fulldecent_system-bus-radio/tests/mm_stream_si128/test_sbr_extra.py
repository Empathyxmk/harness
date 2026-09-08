import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from mm_stream_si128.sbr_testlib import sbr_add

class TestSbrExtra(unittest.TestCase):
    def test_sbr_add(self):
        # Simple addition
        self.assertEqual(sbr_add(2, 3), 5)
        # Negative numbers
        self.assertEqual(sbr_add(-2, -3), -5)
        # Addition with zero
        self.assertEqual(sbr_add(7, 0), 7)
        # Commutativity
        self.assertEqual(sbr_add(4, 9), sbr_add(9, 4))

if __name__ == '__main__':
    unittest.main()
    print("All sbr_add tests passed.")