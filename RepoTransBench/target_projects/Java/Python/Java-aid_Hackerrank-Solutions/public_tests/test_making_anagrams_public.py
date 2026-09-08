from collections import Counter

def make_anagram(s1, s2):
    c1 = Counter(s1)
    c2 = Counter(s2)
    all_keys = set(c1) | set(c2)
    return sum(abs(c1.get(k,0) - c2.get(k,0)) for k in all_keys)

def test_different_letters():
    s1 = "game"
    s2 = "team"
    assert make_anagram(s1, s2) == 3

def test_one_string_empty():
    s1 = "football"
    s2 = ""
    assert make_anagram(s1, s2) == 8

def test_both_strings_the_same():
    s1 = "network"
    s2 = "network"
    assert make_anagram(s1, s2) == 0