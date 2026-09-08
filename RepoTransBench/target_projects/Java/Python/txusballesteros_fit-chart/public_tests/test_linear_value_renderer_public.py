from unittest.mock import MagicMock
from src.fitchart.linear_value_renderer import LinearValueRenderer
from src.fitchart.fake_classes import FitChartValue

class RectF(tuple):
    def __new__(cls, left, top, right, bottom):
        return tuple.__new__(cls, (left, top, right, bottom))

def test_build_path_with_different_start_angle_less_than_seek_builds_arc():
    area = RectF(5, 5, 120, 120)
    value = MagicMock(spec=FitChartValue)
    value.getStartAngle.return_value = 10.0
    value.getSweepAngle.return_value = 30.0
    renderer = LinearValueRenderer(area, value)
    path = renderer.buildPath(0.7, 25.0)
    assert path is not None

def test_build_path_with_different_start_angle_greater_than_seek_returns_null():
    area = RectF(10, 10, 80, 80)
    value = MagicMock(spec=FitChartValue)
    value.getStartAngle.return_value = 60.0
    value.getSweepAngle.return_value = 15.0
    renderer = LinearValueRenderer(area, value)
    path = renderer.buildPath(0.3, 40.0)
    assert path is None

def test_calculate_sweep_angle_branches_with_different_data():
    area = RectF(5, 5, 90, 90)
    value = MagicMock(spec=FitChartValue)
    value.getStartAngle.return_value = 5.0
    value.getSweepAngle.return_value = 25.0
    renderer = LinearValueRenderer(area, value)
    # force totalSizeOfValue > animationSeek
    renderer.buildPath(0.3, 20.0)
    # force totalSizeOfValue <= animationSeek
    renderer.buildPath(0.6, 40.0)