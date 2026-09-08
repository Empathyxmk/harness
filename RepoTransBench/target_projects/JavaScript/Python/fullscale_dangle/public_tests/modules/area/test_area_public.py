import pytest
from src.modules.area.area import area_sum

def test_area_sum_normal():
    assert area_sum([5,6,7]) == 18

def test_area_sum_empty_or_nonarray():
    assert area_sum([]) == 0
    assert area_sum("not-an-array") == 0