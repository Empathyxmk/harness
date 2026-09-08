from src.fitchart.base_renderer import BaseRenderer
from unittest.mock import MagicMock
from src.fitchart.fake_classes import FitChartValue

class RectF(tuple):
    def __new__(cls, left, top, right, bottom):
        return tuple.__new__(cls, (left, top, right, bottom))

class ConcreteRenderer(BaseRenderer):
    def __init__(self, drawing_area, value):
        super().__init__(drawing_area, value)

def test_getters():
    area = RectF(1, 2, 3, 4)
    val = MagicMock(spec=FitChartValue)
    renderer = ConcreteRenderer(area, val)
    assert renderer.getDrawingArea() == area
    assert renderer.getValue() == val