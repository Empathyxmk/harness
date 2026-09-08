import pytest

def remove_vowels(s):
    return ''.join([c for c in s if c not in "aeiouAEIOU"])

def test_PublicKqueueTest_RemoveVowels_Main():
    assert remove_vowels("epoll and kqueue") == "pll nd kq"
    assert remove_vowels("QUEUE") == "Q"
    assert remove_vowels("") == ""

def test_PublicKqueueTest_RemoveVowels_Different():
    assert remove_vowels("algorithm") == "lgrthm"
    assert remove_vowels("xyz") == "xyz"