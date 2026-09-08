import pytest
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

def test_extractOne():
    choices = ["new york jets", "new york giants", "liverpool"]
    query = "new york jets"
    res = process.extractOne(query, choices)
    assert isinstance(res, tuple)
    assert res[0] == "new york jets"

def test_extract_limit_and_processor():
    choices = ["foo Xbar", "bar", "baz"]
    query = "foo bar"
    res = process.extract(query, choices, processor=lambda x: x.lower(), scorer=fuzz.token_sort_ratio, limit=2)
    assert len(res) == 2

def test_extractNone():
    assert process.extractOne(None, None) is None
    assert process.extract(None, None) == []

def test_empty_choices_extractOne():
    assert process.extractOne("a", []) is None
    assert process.extract("a", []) == []

def test_indexed_choices():
    choices = {"a": "foo", "b": "boo"}
    out = process.extractOne("foo", choices)
    assert out[0] == "foo"