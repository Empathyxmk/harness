import pytest
from src.modules.area.area import example_method_area

def test_example_method_area_a_gt_b():
    assert example_method_area(3, 1) == 'a'

def test_example_method_area_a_lt_b():
    assert example_method_area(1, 3) == 'b'

def test_example_method_area_a_eq_b():
    assert example_method_area(2, 2) == 'equal'

def test_example_method_area_defaults():
    assert example_method_area() == 'equal'