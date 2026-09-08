import unittest
import sys
import os

# Ensure src is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from termplotlib import barh

class TestBarh(unittest.TestCase):
    def test_simple_barh(self):
        y = [3, 2, 5]
        x = [1, 2, 3]
        barh.barh(y, x)

if __name__ == "__main__":
    unittest.main()