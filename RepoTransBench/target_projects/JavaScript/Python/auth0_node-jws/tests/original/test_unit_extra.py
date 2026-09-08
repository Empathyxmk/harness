import pytest

def add(a, b):
    return a + b

def is_palindrome(s):
    return s == s[::-1]

def test_add_adds_numbers_correctly():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_is_palindrome_detects_palindromes():
    assert is_palindrome('racecar') is True
    assert is_palindrome('hello') is False
    assert is_palindrome('madam') is True