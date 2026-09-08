import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from randexp.randexp import RandExp

def test_randexp_sugar_extensions_gen():
    re_ = RandExp(r"foo\d{1,2}")
    for _ in range(10):
        s = re_.gen()
        assert RandExp(r"^foo\d{1,2}$").match(s), s

def test_randexp_sugar_extensions_call():
    for _ in range(7):
        s = RandExp.randexp(r"h[ij]{2}")
        assert RandExp(r"^h[ij]{2}$").match(s)

def test_randexp_sugar_extensions_to_string():
    re_ = RandExp(r"taco\d{0,3}")
    result = str(re_)
    assert isinstance(result, str)