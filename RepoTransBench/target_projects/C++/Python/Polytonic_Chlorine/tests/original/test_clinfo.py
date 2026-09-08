import pytest

def tokenize(s):
    return [x for x in s.split(' ') if x]

def test_tokenize_basic():
    v = tokenize("hello world")
    assert len(v) == 2
    assert v[0] == "hello"
    assert v[1] == "world"

def test_tokenize_empty():
    v = tokenize("")
    assert len(v) == 0

def test_tokenize_multiple_spaces():
    v = tokenize("a   b c")
    assert len(v) == 3
    assert v[0] == "a"
    assert v[1] == "b"
    assert v[2] == "c"