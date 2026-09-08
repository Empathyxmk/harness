import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from termplotlib import plot

class TestPlotPublic(unittest.TestCase):
    def test_simple_plot_different_data(self):
        y = [0, 4, 2]
        x = [10, 15, 20]
        plot.plot(y, x)

if __name__ == "__main__":
    unittest.main()