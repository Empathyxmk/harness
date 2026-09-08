from src.fitchart.base_renderer import BaseRenderer
from src.fitchart.fake_classes import FitChartValue

class RectF(tuple):
    def __new__(cls, left, top, right, bottom):
        return tuple.__new__(cls, (left, top, right, bottom))

class TestRenderer(BaseRenderer):
    def __init__(self, drawing_area, value):
        super().__init__(drawing_area, value)

def test_get_drawing_area_and_value_with_different_area_and_value():
    area = RectF(10, 12, 34, 56)
    value = FitChartValue(55, 0xABCDEF)
    renderer = TestRenderer(area, value)
    assert renderer.getDrawingArea() is area
    assert renderer.getValue() is value