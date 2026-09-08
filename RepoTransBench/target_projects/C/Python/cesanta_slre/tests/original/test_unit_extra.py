import pytest
from src.slre.slre import (
    slre_match, SLRE_NO_MATCH, SLRE_INVALID_METACHARACTER, SLRE_UNEXPECTED_QUANTIFIER,
    SLRE_UNBALANCED_BRACKETS, SLRE_INVALID_CHARACTER_SET, SLRE_TOO_MANY_BRANCHES,
    SLRE_TOO_MANY_BRACKETS, SLRE_CAPS_ARRAY_TOO_SMALL, SlreCap
)

def test_unexpected_quantifier():
    assert slre_match("*a", "aa", 2) == SLRE_UNEXPECTED_QUANTIFIER

def test_unbalanced_brackets():
    assert slre_match("abc)", "abc)", 4) == SLRE_UNBALANCED_BRACKETS
    assert slre_match("(abc", "abc", 3) == SLRE_UNBALANCED_BRACKETS

def test_invalid_character_set():
    assert slre_match("[]", "a", 1) == SLRE_INVALID_CHARACTER_SET
    assert slre_match("[z-a]", "a", 1) == SLRE_INVALID_CHARACTER_SET

def test_caps_array_too_small():
    caps = [SlreCap("",0) for _ in range(3)]
    assert slre_match("(a)(b)", "ab", 2, caps, 1) == SLRE_CAPS_ARRAY_TOO_SMALL

def test_too_many_brackets():
    # 100 '(' and 100 ')'
    large_regex = '(' * 100 + ')' * 100
    assert slre_match(large_regex, "", 0) == SLRE_TOO_MANY_BRACKETS

def test_too_many_branches():
    branch_regex = "a|" * 101 + "a"
    assert slre_match(branch_regex, "a", 1) == SLRE_TOO_MANY_BRANCHES

def test_quantifiers():
    assert slre_match("a*", "aaa", 3) == 3
    assert slre_match("a+", "aaa", 3) == 3
    assert slre_match("a?", "a", 1) == 1
    assert slre_match("a?", "", 0) == 0

def test_boundaries():
    assert slre_match("abc$", "abc", 3) == 3

def test_dot_wildcard_newline():
    assert slre_match(".", "\n", 1) == 1  # Python regex . matches \n only if DOTALL

def test_escaped_metacharacters():
    assert slre_match("\\.", ".", 1) == 1
    assert slre_match("\\*", "*", 1) == 1
    assert slre_match("\\+", "+", 1) == 1
    assert slre_match("\\?", "?", 1) == 1

def test_metacharacter_classes():
    assert slre_match("\\s", " ", 1) == 1
    assert slre_match("\\S", "a", 1) == 1
    assert slre_match("\\d", "5", 1) == 1
    assert slre_match("\\b", "\b", 1) == 1
    assert slre_match("\\f", "\f", 1) == 1
    assert slre_match("\\n", "\n", 1) == 1
    assert slre_match("\\r", "\r", 1) == 1
    assert slre_match("\\t", "\t", 1) == 1
    assert slre_match("\\v", "\v", 1) == 1