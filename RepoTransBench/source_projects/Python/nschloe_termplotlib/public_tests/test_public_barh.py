import unittest
import sys
import os

# Ensure src is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from termplotlib import barh

class TestBarhPublic(unittest.TestCase):
    def test_simple_barh_different_data(self):
        y = [6, 1, 4]
        x = [7, 8, 9]
        barh.barh(y, x)

if __name__ == "__main__":
    unittest.main()