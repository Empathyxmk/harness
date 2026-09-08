import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from termplotlib.plot import plot

class TestPlot(unittest.TestCase):
    def test_simple_plot(self):
        y = [2, 3, 1]
        x = [1, 2, 3]
        plot(y, x)

if __name__ == "__main__":
    unittest.main()