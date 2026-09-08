import pytest
import math
from src import utils

def test_truncate_string_should_truncate_different_long_string():
    assert utils.truncate_string('0123456789abcdef', 6) == '012345...'

def test_truncate_string_should_not_truncate_another_short_string():
    assert utils.truncate_string('bcd', 4) == 'bcd'

def test_truncate_string_should_use_default_length_and_public_string():
    s = 'abcdefghijabcdefghijabcdefghijabc'
    result = utils.truncate_string(s)
    assert len(result) >= 6
    assert result.endswith('...')
    base = result[:-3]
    assert len(base) == 20

def test_truncate_string_should_handle_empty_string_public():
    assert utils.truncate_string('', 4) == ''

def test_keep_between_returns_value_within_new_range():
    assert utils.keep_between(2, 8, 5) == 5

def test_keep_between_clamps_below_new_min():
    assert utils.keep_between(2, 8, -1) == 2

def test_keep_between_clamps_above_new_max():
    assert utils.keep_between(2, 8, 42) == 8

def test_get_position_from_angle_and_distance_180_deg():
    x, y = utils.get_position_from_angle_and_distance(180, 4)
    assert math.isclose(x, -4)
    assert math.isclose(y, 0)

def test_get_position_from_angle_and_distance_270_deg():
    x, y = utils.get_position_from_angle_and_distance(270, 7)
    assert math.isclose(x, 0, abs_tol=1e-5)
    assert math.isclose(y, -7, abs_tol=1e-5)

def test_get_angle_from_position_0_minus1():
    angle = utils.get_angle_from_position(0, -1)
    assert math.isclose(angle, 270)

def test_get_angle_from_position_1_1():
    angle = utils.get_angle_from_position(1, 1)
    assert math.isclose(angle, 45)

def test_get_angle_from_position_minus1_minus1():
    angle = utils.get_angle_from_position(-1, -1)
    assert math.isclose(angle, -135)

def test_keep_circle_inside_circle_returns_position_unchanged_if_already_inside():
    assert utils.keep_circle_inside_circle(7, [1,2], 1, [2,3]) == [2,3]

def test_keep_circle_inside_circle_repositions_if_clearly_outside():
    v = utils.keep_circle_inside_circle(6, [0,0], 1, [8, 0])
    assert v[0] < 6

def test_keep_circle_inside_circle_pads_more_for_negative_angles_isparent():
    res = utils.keep_circle_inside_circle(6, [0,0], 1, [-2,-5], True)
    assert isinstance(res, list)