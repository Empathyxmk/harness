import pytest

class ExpandAnimationUtils:
    @staticmethod
    def getWidthAfterCollapse(initial_width, delta_width):
        return initial_width - delta_width

    @staticmethod
    def getWidthAfterExpand(initial_width, delta_width):
        return initial_width + delta_width

def test_get_width_after_collapse_with_other_params():
    initial_width = 100
    delta_width = 25
    expected = 75
    result = ExpandAnimationUtils.getWidthAfterCollapse(initial_width, delta_width)
    assert result == expected

def test_get_width_after_expand_with_other_params():
    initial_width = 150
    delta_width = 45
    expected = 195
    result = ExpandAnimationUtils.getWidthAfterExpand(initial_width, delta_width)
    assert result == expected