import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import termplotlib.plot as plot

class TestScatterPublic(unittest.TestCase):
    def test_simple_scatter_different_data(self):
        x = [4, 5, 6]
        y = [6, 5, 4]
        plot.plot(y, x)

if __name__ == "__main__":
    unittest.main()