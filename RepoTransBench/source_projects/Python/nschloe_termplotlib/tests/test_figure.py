import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from termplotlib.figure import Figure

class TestFigure(unittest.TestCase):
    def test_figure_init(self):
        fig = Figure()
        self.assertIsInstance(fig, Figure)

if __name__ == "__main__":
    unittest.main()