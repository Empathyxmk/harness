import pytest
from termplotlib import figure

class TestFigurePublic:
    def test_figure_creation_and_axes(self):
        f = figure.Figure()
        # Add an axis and ensure it's an Axes object
        ax = f.add_subplot(111)
        from termplotlib.figure import Axes
        assert isinstance(ax, Axes)
        # Add a second axis and test it's also an Axes object
        ax2 = f.add_subplot(112)
        assert isinstance(ax2, Axes)
        # Check different axes are not the same
        assert ax != ax2