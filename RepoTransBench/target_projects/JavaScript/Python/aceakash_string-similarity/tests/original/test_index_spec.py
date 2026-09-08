import pytest
from src import findBestMatch

bad_args_msg = 'Bad arguments: First argument should be a string, second should be an array of strings'

def test_find_best_match_throws_if_no_args():
    with pytest.raises(ValueError) as exc:
        findBestMatch()
    assert bad_args_msg in str(exc.value)

def test_find_best_match_throws_if_first_arg_not_string():
    with pytest.raises(ValueError) as exc:
        findBestMatch(8)
    assert bad_args_msg in str(exc.value)
    with pytest.raises(ValueError) as exc:
        findBestMatch({})
    assert bad_args_msg in str(exc.value)

def test_find_best_match_throws_if_second_arg_not_array():
    with pytest.raises(ValueError) as exc:
        findBestMatch('hello', 'something')
    assert bad_args_msg in str(exc.value)
    with pytest.raises(ValueError) as exc:
        findBestMatch('hello', {})
    assert bad_args_msg in str(exc.value)

def test_find_best_match_throws_if_second_arg_not_array_of_strings():
    with pytest.raises(ValueError) as exc:
        findBestMatch('hello', [2, 'something'])
    assert bad_args_msg in str(exc.value)

def test_find_best_match_assigns_similarity_rating_to_each_string():
    result = findBestMatch('healed', ['edward', 'sealed', 'theatre'])
    assert [{ 'target': rating['target'], 'rating': type(rating['rating']) }
            for rating in result['ratings']
         ] == [
        {'target': 'edward', 'rating': float},
        {'target': 'sealed', 'rating': float},
        {'target': 'theatre', 'rating': float}
    ]

def test_find_best_match_returns_best_match_object():
    result = findBestMatch('healed', ['edward', 'sealed', 'theatre'])
    assert result['bestMatch']['target'] == 'sealed'

def test_find_best_match_returns_best_match_index():
    result = findBestMatch('healed', ['edward', 'sealed', 'theatre'])
    assert result['bestMatchIndex'] == 1