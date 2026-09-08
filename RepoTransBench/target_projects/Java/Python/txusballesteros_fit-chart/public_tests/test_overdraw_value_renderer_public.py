from unittest.mock import MagicMock
from src.fitchart.overdraw_value_renderer import OverdrawValueRenderer
from src.fitchart.fake_classes import FitChartValue

class RectF(tuple):
    def __new__(cls, left, top, right, bottom):
        return tuple.__new__(cls, (left, top, right, bottom))

def test_build_path_with_other_angles():
    area = RectF(2, 2, 50, 50)
    value = MagicMock(spec=FitChartValue)
    value.getStartAngle.return_value = 30.0
    value.getSweepAngle.return_value = 45.0
    renderer = OverdrawValueRenderer(area, value)
    path = renderer.buildPath(0.6, 35.0)
    assert path is not None