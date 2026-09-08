import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from mm_stream_si128.sbr_testlib import sbr_add

class TestSbr(unittest.TestCase):
    def test_add_zero(self):
        self.assertEqual(sbr_add(0, 0), 0)
        self.assertEqual(sbr_add(123, 0), 123)
        self.assertEqual(sbr_add(0, 456), 456)
    
    def test_add_negative(self):
        self.assertEqual(sbr_add(-1, -2), -3)
        self.assertEqual(sbr_add(-10, 5), -5)

if __name__ == '__main__':
    unittest.main()