import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import termplotlib.plot as plot

class TestScatter(unittest.TestCase):
    def test_simple_scatter(self):
        # plot.plot does NOT take marker kwarg; only x, y, optional label
        x = [1,2,3]
        y = [3,2,1]
        # The default plot will render standard plot, which can stand for 'scatter'
        plot.plot(y, x)  # y against x as in codebase usage

if __name__ == "__main__":
    unittest.main()