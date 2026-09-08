import pytest
from src import findBestMatch

def test_find_best_match_should_handle_identical_strings_public():
    result = findBestMatch('goodbye', ['goodbye', 'cruel world'])
    assert result['bestMatch']['target'] == 'goodbye'
    assert pytest.approx(result['ratings'][0]['rating'], 0.01) == 1

def test_find_best_match_should_handle_non_string_input_public():
    with pytest.raises(Exception):
        findBestMatch(None, ['xyz'])
    with pytest.raises(Exception):
        findBestMatch(None, ['xyz'])
    with pytest.raises(Exception):
        findBestMatch('xyz', [None])

def test_find_best_match_should_give_best_match_from_possible_ties_public():
    targets = ['tie', 'tie', 'untie']
    input_string = 'tie'
    result = findBestMatch(input_string, targets)
    assert result['bestMatch']['target'] == 'tie'
    assert sum(1 for r in result['ratings'] if r['rating'] == 1) > 0

def test_find_best_match_should_handle_similar_non_equal_multi_word_strings_public():
    input_string = 'baz foo bar'
    options = ['baz foo jar', 'foo bar', 'bar baz boo']
    result = findBestMatch(input_string, options)
    assert result['bestMatch']['target'] in options