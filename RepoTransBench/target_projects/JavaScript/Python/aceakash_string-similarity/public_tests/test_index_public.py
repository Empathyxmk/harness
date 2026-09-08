import pytest
from src import compareTwoStrings, findBestMatch

def test_compare_two_strings_identical_public():
    assert compareTwoStrings('abc123', 'abc123') == 1

def test_compare_two_strings_completely_different_public():
    assert compareTwoStrings('dog', 'cat') == 0

def test_compare_two_strings_partial_overlap_public():
    result = compareTwoStrings('marvelous', 'marvel')
    assert result > 0
    assert result < 1

def test_compare_two_strings_empty_strings_public():
    assert compareTwoStrings('', '') == 1
    assert compareTwoStrings('test', '') == 0
    assert compareTwoStrings('', 'test') == 0

def test_find_best_match_best_match_in_array_public():
    main = "baker"
    matches = ["maker", "faker", "taker", "baker"]
    output = findBestMatch(main, matches)
    assert output['bestMatch']['target'] == "baker"
    assert isinstance(output['ratings'], list)
    assert len(output['ratings']) == 4

def test_find_best_match_handles_bad_argument_types_public():
    with pytest.raises(Exception):
        findBestMatch(None, None)
    with pytest.raises(Exception):
        findBestMatch('world', None)
    with pytest.raises(Exception):
        findBestMatch('world', 10)
    with pytest.raises(Exception):
        findBestMatch('world', ['a', True])
    with pytest.raises(Exception):
        findBestMatch('world', [])