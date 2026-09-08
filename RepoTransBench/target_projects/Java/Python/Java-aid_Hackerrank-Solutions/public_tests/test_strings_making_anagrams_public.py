from collections import Counter

def number_needed(s1, s2):
    c1, c2 = Counter(s1), Counter(s2)
    return sum(abs(c1.get(k,0) - c2.get(k,0)) for k in set(c1) | set(c2))

def test_no_overlap():
    s1 = "abcxyz"
    s2 = "defuvw"
    assert number_needed(s1, s2) == 12

def test_partial_overlap():
    s1 = "banana"
    s2 = "bandana"
    assert number_needed(s1, s2) == 2

def test_one_empty():
    s1 = "laptop"
    s2 = ""
    assert number_needed(s1, s2) == 6