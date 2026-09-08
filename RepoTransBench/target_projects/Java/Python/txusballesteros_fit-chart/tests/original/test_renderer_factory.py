from unittest.mock import MagicMock
from src.fitchart.renderer_factory import RendererFactory
from src.fitchart.fake_classes import AnimationMode, FitChartValue
from src.fitchart.linear_value_renderer import LinearValueRenderer
from src.fitchart.overdraw_value_renderer import OverdrawValueRenderer

class RectF(tuple):
    def __new__(cls, left, top, right, bottom):
        return tuple.__new__(cls, (left, top, right, bottom))

def test_returns_linear_renderer():
    value = MagicMock(spec=FitChartValue)
    rect = RectF(0, 0, 100, 100)
    renderer = RendererFactory.getRenderer(AnimationMode.LINEAR, value, rect)
    assert isinstance(renderer, LinearValueRenderer)

def test_returns_overdraw_renderer():
    value = MagicMock(spec=FitChartValue)
    rect = RectF(0, 0, 100, 100)
    renderer = RendererFactory.getRenderer(AnimationMode.OVERDRAW, value, rect)
    assert isinstance(renderer, OverdrawValueRenderer)