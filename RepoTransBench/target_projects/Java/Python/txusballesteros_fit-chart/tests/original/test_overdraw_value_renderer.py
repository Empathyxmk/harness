from unittest.mock import MagicMock
from src.fitchart.overdraw_value_renderer import OverdrawValueRenderer
from src.fitchart.fake_classes import FitChartValue

class RectF(tuple):
    def __new__(cls, left, top, right, bottom):
        return tuple.__new__(cls, (left, top, right, bottom))

def test_build_path():
    area = RectF(0, 0, 100, 100)
    value = MagicMock(spec=FitChartValue)
    value.getStartAngle.return_value = 10.0
    value.getSweepAngle.return_value = 100.0
    renderer = OverdrawValueRenderer(area, value)
    path = renderer.buildPath(0.5, 50.0)
    assert path is not None