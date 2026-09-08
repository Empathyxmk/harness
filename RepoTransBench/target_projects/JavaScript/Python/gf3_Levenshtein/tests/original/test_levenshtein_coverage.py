import pytest
from src.levenshtein import levenshtein

def test_levenshtein_identical_strings():
    assert levenshtein('abc', 'abc') == 0

def test_levenshtein_completely_different_strings():
    assert levenshtein('abc', 'xyz') == 3

def test_levenshtein_with_substring():
    assert levenshtein('kitten', 'kit') == 3
    assert levenshtein('kit', 'kitten') == 3

def test_levenshtein_with_one_empty():
    assert levenshtein('', 'abc') == 3
    assert levenshtein('abc', '') == 3

def test_levenshtein_with_both_empty():
    assert levenshtein('', '') == 0

def test_levenshtein_single_replace():
    assert levenshtein('a', 'b') == 1

def test_levenshtein_add_delete_replace():
    assert levenshtein('abc', 'ab') == 1  # delete
    assert levenshtein('ab', 'abc') == 1  # add
    assert levenshtein('abc', 'adc') == 1  # replace
    assert levenshtein('abc', 'axc') == 1  # replace
    assert levenshtein('abcdef', 'azced') == 3  # complex

def test_levenshtein_equal_length_totally_different():
    assert levenshtein('cat', 'dog') == 3

def test_levenshtein_unicode():
    assert levenshtein('mañana', 'manana') == 1
    assert levenshtein('🙂', '🙃') == 1