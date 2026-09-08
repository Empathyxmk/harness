import pytest
from src import findBestMatch

bad_args_msg = 'Bad arguments: First argument should be a string, second should be an array of strings'

def test_find_best_match_throws_if_no_args_public():
    with pytest.raises(ValueError) as exc:
        findBestMatch()
    assert bad_args_msg in str(exc.value)

def test_find_best_match_throws_if_first_arg_not_string_public():
    with pytest.raises(ValueError) as exc:
        findBestMatch(True)
    assert bad_args_msg in str(exc.value)
    with pytest.raises(ValueError) as exc:
        findBestMatch([])
    assert bad_args_msg in str(exc.value)

def test_find_best_match_throws_if_second_arg_not_array_public():
    with pytest.raises(ValueError) as exc:
        findBestMatch('sample', 'item')
    assert bad_args_msg in str(exc.value)
    with pytest.raises(ValueError) as exc:
        findBestMatch('sample', 123)
    assert bad_args_msg in str(exc.value)

def test_find_best_match_throws_if_second_arg_not_array_of_strings_public():
    with pytest.raises(ValueError) as exc:
        findBestMatch('sample', [{}, 'item'])
    assert bad_args_msg in str(exc.value)

def test_find_best_match_assigns_similarity_rating_to_each_string_public():
    result = findBestMatch('marker', ['baker', 'maker', 'faker'])
    assert [{ 'target': rating['target'], 'rating': type(rating['rating']) }
            for rating in result['ratings']
         ] == [
        {'target': 'baker', 'rating': float},
        {'target': 'maker', 'rating': float},
        {'target': 'faker', 'rating': float}
    ]

def test_find_best_match_returns_best_match_object_public():
    result = findBestMatch('marker', ['baker', 'maker', 'faker'])
    assert result['bestMatch']['target'] == 'maker'

def test_find_best_match_returns_best_match_index_public():
    result = findBestMatch('marker', ['baker', 'maker', 'faker'])
    assert result['bestMatchIndex'] == 1