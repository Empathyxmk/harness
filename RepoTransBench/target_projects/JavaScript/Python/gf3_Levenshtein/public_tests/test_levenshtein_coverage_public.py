import pytest
from src.levenshtein import levenshtein

def test_levenshtein_empty_strings_public():
    assert levenshtein('', '') == 0
    assert levenshtein('abc', '') == 3
    assert levenshtein('', 'xyz') == 3

def test_levenshtein_identical_strings_public():
    assert levenshtein('good', 'good') == 0

def test_levenshtein_pure_insert_public():
    assert levenshtein('red', 'ready') == 2
    assert levenshtein('go', 'gone') == 2

def test_levenshtein_pure_delete_public():
    assert levenshtein('testing', 'test') == 3

def test_levenshtein_substitution_public():
    assert levenshtein('like', 'bike') == 1

def test_levenshtein_simple_diff_public():
    assert levenshtein('hat', 'what') == 1

def test_levenshtein_single_substitution_equal_length_public():
    assert levenshtein('glass', 'grass') == 1

def test_levenshtein_double_insertion_public():
    assert levenshtein('sing', 'signal') == 3

def test_levenshtein_swapped_characters_public():
    assert levenshtein('form', 'from') == 2

def test_levenshtein_equal_length_totally_different_public():
    assert levenshtein('car', 'dog') == 3

def test_levenshtein_unicode_public():
    assert levenshtein('mañana', 'manana') == 1
    assert levenshtein('🏀', '⚽️') == 2