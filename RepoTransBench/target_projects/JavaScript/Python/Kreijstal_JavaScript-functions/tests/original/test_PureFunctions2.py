import pytest
from src.PureFunctions2 import (
    mapValueWithInstructions,
    stretchTileFunction,
    coordinatesToIndex,
    indexToCoordinates,
)

class TestMapValueWithInstructions:
    def test_swaps_values_according_to_sortOrder_simple_numbers(self):
        assert mapValueWithInstructions(1, [1,2], [2,1]) == 2
        assert mapValueWithInstructions(2, [1,2], [2,1]) == 1
        assert mapValueWithInstructions(3, [1,2], [2,1]) == 3

    def test_returns_mapped_value_for_string_match(self):
        assert mapValueWithInstructions(
            'findThisElement',
            ['in this list','findThisElement'],
            ['and replace it','with the index it found']
        ) == 'with the index it found'

    def test_works_with_finder_functions_and_result_functions(self):
        rockObj = { "object": "rock" }
        cloudObj = { "object": "cloud" }
        def finder_rock(a): return a["object"] == "rock"
        def finder_cloud(a): return a["object"] == "cloud"
        def make_cloud(a): a["object"] = "cloud"; return a
        def make_rock(a): a["object"] = "rock"; return a

        result1 = mapValueWithInstructions(
            {"object": "rock"},
            [finder_rock, finder_cloud],
            [make_cloud, make_rock],
        )
        assert result1["object"] == "cloud"

        result2 = mapValueWithInstructions(
            {"object": "cloud"},
            [finder_rock, finder_cloud],
            [make_cloud, make_rock],
        )
        assert result2["object"] == "rock"

    def test_returns_original_value_if_not_found(self):
        assert mapValueWithInstructions('nope', ['hello','world'], [1,2]) == 'nope'


class TestStretchTileFunction:
    def test_should_call_callback_with_floored_values(self):
        calls = {}
        def cb(x, y): 
            calls['x'] = x
            calls['y'] = y
        stretch = stretchTileFunction(cb, 2, 3)
        stretch(5,8)
        assert 'x' in calls and 'y' in calls
        assert calls['x'] == 2
        assert calls['y'] == 2

    def test_should_return_callback_result(self):
        stretch = stretchTileFunction(lambda x, y: f"A-{x},{y}", 2,2)
        assert stretch(4,6) == 'A-2,3'


class TestCoordinatesToIndex:
    def test_returns_correct_index_for_2D_point(self):
        assert coordinatesToIndex(2, 1, 5) == 7
        assert coordinatesToIndex(0, 0, 5) == 0
        assert coordinatesToIndex(5, 2, 3) == 5%3 + 2*3


class TestIndexToCoordinates:
    def test_returns_correct_xy_from_index(self):
        assert indexToCoordinates(7, 5) == (2,1)
        assert indexToCoordinates(0, 5) == (0,0)
        assert indexToCoordinates(8, 3) == (2,2)