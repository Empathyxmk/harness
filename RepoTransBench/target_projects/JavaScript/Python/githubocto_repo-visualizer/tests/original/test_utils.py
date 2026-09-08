import pytest
import math
from src import utils

def test_truncate_string_should_truncate_long_strings_and_append():
    assert utils.truncate_string('abcdefghijklmnopqrstuvwxyz', 5) == 'abcde...'

def test_truncate_string_should_not_truncate_short_string():
    assert utils.truncate_string('abc', 5) == 'abc'

def test_truncate_string_should_use_default_length_20():
    result = utils.truncate_string('abcdefghijklmnopqrsuvwxyz')
    assert len(result) >= 6  # Should at least match regex: \w{20}\.\.\.$
    assert result.endswith('...')
    base = result[:-3]
    assert len(base) == 20

def test_truncate_string_should_handle_empty_string():
    assert utils.truncate_string('', 10) == ''

def test_keep_between_returns_within_range():
    assert utils.keep_between(0, 10, 5) == 5

def test_keep_between_clamps_below_min():
    assert utils.keep_between(0, 10, -2) == 0

def test_keep_between_clamps_above_max():
    assert utils.keep_between(0, 10, 42) == 10

def test_get_position_from_angle_and_distance_zero_deg():
    x, y = utils.get_position_from_angle_and_distance(0, 10)
    assert math.isclose(x, 10)
    assert math.isclose(y, 0)

def test_get_position_from_angle_and_distance_ninety_deg():
    x, y = utils.get_position_from_angle_and_distance(90, 20)
    assert math.isclose(x, 0, abs_tol=1e-5)
    assert math.isclose(y, 20, abs_tol=1e-5)

def test_get_angle_from_position_1_0():
    angle = utils.get_angle_from_position(1, 0)
    assert math.isclose(angle, 0)

def test_get_angle_from_position_0_1():
    angle = utils.get_angle_from_position(0, 1)
    assert math.isclose(angle, 90)

def test_get_angle_from_position_minus1_0():
    angle = utils.get_angle_from_position(-1, 0)
    assert math.isclose(angle, 180)

def test_keep_circle_inside_circle_returns_unchanged_if_inside():
    assert utils.keep_circle_inside_circle(10, [0,0], 1, [1,1]) == [1,1]

def test_keep_circle_inside_circle_repositions_if_outside():
    v = utils.keep_circle_inside_circle(10, [0,0], 2, [20, 0])
    assert v[0] < 10  # X coordinate should be less than outer circle radius

def test_keep_circle_inside_circle_pads_more_for_certain_angles_isparent():
    res = utils.keep_circle_inside_circle(10, [0,0], 2, [-1, -8], True)
    assert isinstance(res, list)