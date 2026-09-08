import pytest
from jd4 import case

def test_case_repr_diff_params():
    # Use different data than existing test for public test
    c = case.Case("test_case2", "input-42", "output-99", score=15)
    r = repr(c)
    assert "test_case2" in r
    assert "score=15" in r

def test_case_properties_different():
    c = case.Case("sampleB", "abc", "def", score=8)
    assert c.name == "sampleB"
    assert c.input == "abc"
    assert c.output == "def"
    assert c.score == 8

def test_case_eq_false():
    # Different object, string comparison must be False
    c = case.Case("eqtest2", "in", "out", score=1)
    assert not (c == 42)
    assert c != 42

def test_case_ordering_different_name():
    c1 = case.Case("case0002", "", "", score=0)
    c2 = case.Case("case0010", "", "", score=0)
    assert c1 < c2

def test_case_str_content():
    c = case.Case("visible2", "inputY", "outputY", score=4)
    s = str(c)
    assert "visible2" in s and "inputY" in s and "outputY" in s and "score=4" in s