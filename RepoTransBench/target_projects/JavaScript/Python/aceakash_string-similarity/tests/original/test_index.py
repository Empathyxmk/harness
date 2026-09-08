import pytest
from src import compareTwoStrings, findBestMatch

def test_compare_two_strings_identical():
    assert compareTwoStrings('hello', 'hello') == 1

def test_compare_two_strings_completely_different():
    assert compareTwoStrings('foo', 'bar') == 0

def test_compare_two_strings_partial_overlap():
    result = compareTwoStrings('hello', 'yellow')
    assert result > 0
    assert result < 1

def test_compare_two_strings_empty_strings():
    assert compareTwoStrings('', '') == 1
    assert compareTwoStrings('nonempty', '') == 0
    assert compareTwoStrings('', 'nonempty') == 0

def test_find_best_match_best_match_in_array():
    main = "healed"
    matches = ["edward", "sealed", "theatre", "healed"]
    output = findBestMatch(main, matches)
    assert output['bestMatch']['target'] == "healed"
    assert isinstance(output['ratings'], list)
    assert len(output['ratings']) == 4

def test_find_best_match_handles_bad_argument_types():
    with pytest.raises(Exception):
        findBestMatch(None, None)
    with pytest.raises(Exception):
        findBestMatch('hello', None)
    with pytest.raises(Exception):
        findBestMatch('hello', 42)
    with pytest.raises(Exception):
        findBestMatch('hello', ['a', 42])
    with pytest.raises(Exception):
        findBestMatch('hello', [])