import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from termplotlib import hist

class TestHist(unittest.TestCase):
    def test_simple_hist(self):
        data = [1, 2, 2, 3]
        bin_edges = [1, 2, 3]
        hist.hist(data, bin_edges)  # pass required bin_edges argument

if __name__ == "__main__":
    unittest.main()