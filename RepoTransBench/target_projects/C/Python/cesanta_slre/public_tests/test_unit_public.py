import pytest
from src.slre.slre import (
    slre_match, SLRE_NO_MATCH, SLRE_INVALID_METACHARACTER,
    SLRE_IGNORE_CASE, SlreCap
)

def test_simple_matching():
    assert slre_match("cat", "A wild cat appears", 18) == 3
    assert slre_match("dog", "The dog barked!", 15) == 3
    assert slre_match("bird", "This is a blue bird.", 20) == 4

def test_group_capture_email():
    caps = [SlreCap("",0) for _ in range(10)]
    assert slre_match("mail:(\\w+@\\w+\\.\\w+)", "mail:jane123@xyz.org ;next", 25, caps, 10) == 16
    assert caps[0].len == 13
    assert caps[0].ptr == "jane123@xyz.org"

def test_chars_and_quantifiers():
    assert slre_match("[.9]", "B9K", 3) == 2
    assert slre_match("t+", "teeeeeest", 9) == 1
    assert slre_match("e+", "teeeeeest", 9) == 6
    assert slre_match("m*", "mmmmoo", 6) == 4

def test_dot_wildcard():
    assert slre_match("f.g", "fig frog fog", 11) == 3

def test_w_and_W():
    assert slre_match("[\\w]+", "ZXCV_92", 7) == 7
    assert slre_match("[\\W]+", "!!!", 3) == 3

def test_S_class():
    assert slre_match("[\\S]+", "JKL345", 6) == 6

def test_alternation_startswith():
    assert slre_match("apples|oranges", "I like oranges best", 20) == 7

def test_nested_capture_group():
    caps = [SlreCap("",0) for _ in range(10)]
    assert slre_match("([A-Z][a-z]+) ([A-Z][a-z]+)", "Jane Smith", 10, caps, 10) == 10
    assert caps[0].len == 4 and caps[0].ptr == "Jane"
    assert caps[1].len == 5 and caps[1].ptr == "Smith"

def test_anchors():
    assert slre_match("^Qwerty$", "Qwerty", 6) == 6

def test_zero_width_lookahead():
    assert slre_match("(?!)", "notused", 7) == SLRE_INVALID_METACHARACTER

def test_numeric_class_input():
    assert slre_match("\\d+", "555xyz", 6) == 3

def test_optional_quantifier_space():
    assert slre_match("a? b", " b", 2) == 2

def test_set_at_end():
    assert slre_match("[jklmn]+$", "DARKmjnkl", 9) == 5