import pytest

def tokenize(s):
    return [x for x in s.split(',') if x]

def test_tokenize_basic():
    v = tokenize("foo,bar")
    assert len(v) == 2
    assert v[0] == "foo"
    assert v[1] == "bar"

def test_tokenize_empty():
    v = tokenize("")
    assert len(v) == 0

def test_tokenize_multiple_commas():
    v = tokenize("a,,,b,c")
    assert len(v) == 3
    assert v[0] == "a"
    assert v[1] == "b"
    assert v[2] == "c"