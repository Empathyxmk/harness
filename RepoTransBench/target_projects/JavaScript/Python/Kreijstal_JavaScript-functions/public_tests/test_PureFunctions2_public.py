import pytest
from src.PureFunctions2 import (
    mapValueWithInstructions,
    stretchTileFunction,
    coordinatesToIndex,
    indexToCoordinates,
)

def test_swaps_values_with_different_numbers():
    assert mapValueWithInstructions(10, [10, 20], [20, 10]) == 20
    assert mapValueWithInstructions(20, [10, 20], [20, 10]) == 10
    assert mapValueWithInstructions(99, [10,20], [20,10]) == 99

def test_maps_value_for_different_string_match():
    assert mapValueWithInstructions(
        'searchThisString',
        ['containsThis','searchThisString'],
        ['output1','found value']
    ) == 'found value'

def test_works_with_alternate_finder_and_result_functions():
    appleObj = { "fruit": "apple" }
    bananaObj = { "fruit": "banana" }
    def finder_apple(a): return a["fruit"] == "apple"
    def finder_banana(a): return a["fruit"] == "banana"
    def make_banana(a): a["fruit"] = "banana"; return a
    def make_apple(a): a["fruit"] = "apple"; return a

    result1 = mapValueWithInstructions(
        {"fruit": "apple"},
        [finder_apple, finder_banana],
        [make_banana, make_apple],
    )
    assert result1["fruit"] == "banana"

    result2 = mapValueWithInstructions(
        {"fruit": "banana"},
        [finder_apple, finder_banana],
        [make_banana, make_apple],
    )
    assert result2["fruit"] == "apple"

def test_returns_original_value_if_value_not_mapped():
    assert mapValueWithInstructions('absent', ['first','second'], [100,200]) == 'absent'

def test_should_call_callback_with_different_floored_values():
    calls = {}
    def cb(x, y): 
        calls['x'] = x
        calls['y'] = y
    stretch = stretchTileFunction(cb, 3, 4)
    stretch(7,13)
    assert calls['x'] == 2
    assert calls['y'] == 3

def test_should_return_altered_callback_result():
    stretch = stretchTileFunction(lambda x, y: f"B-{x}:{y}", 4,5)
    assert stretch(12,16) == "B-3:3"

def test_returns_correct_index_for_different_2d_point():
    assert coordinatesToIndex(3, 2, 7) == 17
    assert coordinatesToIndex(1, 0, 6) == 1
    assert coordinatesToIndex(8, 4, 5) == 8%5 + 4*5

def test_returns_correct_xy_from_different_index_values():
    assert indexToCoordinates(17, 7) == (3,2)
    assert indexToCoordinates(1, 6) == (1,0)
    assert indexToCoordinates(14, 5) == (4,2)