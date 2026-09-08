from unittest.mock import MagicMock
from src.fitchart.renderer_factory import RendererFactory
from src.fitchart.fake_classes import AnimationMode, FitChartValue
from src.fitchart.linear_value_renderer import LinearValueRenderer
from src.fitchart.overdraw_value_renderer import OverdrawValueRenderer

class RectF(tuple):
    def __new__(cls, left, top, right, bottom):
        return tuple.__new__(cls, (left, top, right, bottom))

def test_create_renderer_returns_linear_value_renderer_with_different_area():
    value = MagicMock(spec=FitChartValue)
    area = RectF(1, 2, 80, 60)
    renderer = RendererFactory.create(area, value, AnimationMode.LINEAR)
    assert isinstance(renderer, LinearValueRenderer)

def test_create_renderer_returns_overdraw_value_renderer_with_different_area():
    value = MagicMock(spec=FitChartValue)
    area = RectF(3, 4, 70, 30)
    renderer = RendererFactory.create(area, value, AnimationMode.OVERDRAW)
    assert isinstance(renderer, OverdrawValueRenderer)