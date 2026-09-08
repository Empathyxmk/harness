import pytest
from src.spellfucker import spellfucker

def test_mutate_simple_word_hello():
    result = spellfucker('hello')
    assert result != 'hello'
    assert isinstance(result, str)

def test_multiline_works():
    s = 'hello\nworld'
    res = spellfucker(s)
    assert len(res.split('\n')) == 2

def test_with_empty_string():
    assert spellfucker('') == ''

def test_null_undefined_should_not_throw():
    assert spellfucker(None) == ''
    # Python doesn't have undefined, check None again
    assert spellfucker(None) == ''

def test_not_mutate_punctuation():
    assert spellfucker('..,!?') == '..,!?'

def test_not_overly_shrink_words():
    orig = 'bananana'
    res = spellfucker(orig)
    assert len(res) > 0
    assert abs(len(res) - len(orig)) < len(orig)

def test_mutate_multiple_words_sentence():
    s = 'This is an example sentence.'
    m = spellfucker(s)
    assert len(m) > 0
    assert m != s

def test_no_error_on_gibberish():
    res = spellfucker('asdklj2398u4__--==++')
    assert isinstance(res, str)

def test_no_error_on_whitespace_only():
    assert spellfucker('    \n \t') == '    \n \t'