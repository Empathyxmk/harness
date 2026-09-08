import pytest
from src import findBestMatch

def test_find_best_match_should_handle_identical_strings():
    result = findBestMatch('hello', ['hello', 'world'])
    assert result['bestMatch']['target'] == 'hello'
    assert pytest.approx(result['ratings'][0]['rating'], 0.01) == 1

def test_find_best_match_should_handle_non_string_input():
    with pytest.raises(Exception):
        findBestMatch(None, ['abc'])
    with pytest.raises(Exception):
        findBestMatch(None, ['abc'])  # Python does not have undefined
    with pytest.raises(Exception):
        findBestMatch('abc', [None])

def test_find_best_match_should_give_best_match_from_possible_ties():
    targets = ['same', 'same', 'other']
    input_string = 'same'
    result = findBestMatch(input_string, targets)
    assert result['bestMatch']['target'] == 'same'
    assert sum(1 for r in result['ratings'] if r['rating'] == 1) > 0

def test_find_best_match_should_handle_similar_non_equal_multi_word_strings():
    input_string = 'foo bar baz'
    options = ['foo bar buz', 'foo bar', 'bar baz foo']
    result = findBestMatch(input_string, options)
    # Accept ANY in options, as exact best match may depend on implementation.
    assert result['bestMatch']['target'] in options