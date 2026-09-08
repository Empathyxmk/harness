import pytest

# Placeholder implementation as per function names, must be replaced with actual ones
def to_lower(s):
    s[0] = s[0].lower()

def to_upper(s):
    s[0] = s[0].upper()

def trim(s):
    s[0] = s[0].strip()

def split(s, delimiter):
    return s.split(delimiter)

def join(words, delimiter):
    return delimiter.join(words)

def test_to_lower_case():
    s = ["PublicTEST"]
    to_lower(s)
    assert s[0] == "publictest"

def test_to_upper_case():
    s = ["anotherCase"]
    to_upper(s)
    assert s[0] == "ANOTHERCASE"

def test_trim_test():
    s = [" \t\ntrim here\t\n "]
    trim(s)
    assert s[0] == "trim here"

def test_split_test():
    s = "alpha,beta,gamma"
    v = split(s, ',')
    assert len(v) == 3
    assert v[0] == "alpha"
    assert v[2] == "gamma"

def test_join_test():
    v = ["join", "these", "words"]
    s = join(v, '-')
    assert s == "join-these-words"