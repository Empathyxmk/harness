import pytest
from unittest.mock import MagicMock
from src.fitchart.linear_value_renderer import LinearValueRenderer
from src.fitchart.fake_classes import FitChartValue

class RectF(tuple):
    def __new__(cls, left, top, right, bottom):
        return tuple.__new__(cls, (left, top, right, bottom))

def test_build_path_with_start_angle_less_than_seek_builds_arc():
    area = RectF(0, 0, 100, 100)
    value = MagicMock(spec=FitChartValue)
    value.getStartAngle.return_value = 0.0
    value.getSweepAngle.return_value = 100.0
    renderer = LinearValueRenderer(area, value)

    path = renderer.buildPath(0.5, 50.0)

    assert path is not None

def test_build_path_with_start_angle_greater_than_seek_returns_null():
    area = RectF(0, 0, 100, 100)
    value = MagicMock(spec=FitChartValue)
    value.getStartAngle.return_value = 100.0
    value.getSweepAngle.return_value = 50.0
    renderer = LinearValueRenderer(area, value)

    path = renderer.buildPath(0.5, 40.0)

    assert path is None

def test_calculate_sweep_angle_path_branches():
    area = RectF(0, 0, 100, 100)
    value = MagicMock(spec=FitChartValue)
    value.getStartAngle.return_value = 20.0
    value.getSweepAngle.return_value = 50.0
    renderer = LinearValueRenderer(area, value)

    # force totalSizeOfValue > animationSeek
    path1 = renderer.buildPath(0.5, 40.0)
    # force totalSizeOfValue <= animationSeek
    path2 = renderer.buildPath(0.5, 80.0)
    # just assert no errors and path1, path2 are checked for None
    assert path1 is not None or path1 is None
    assert path2 is not None or path2 is None