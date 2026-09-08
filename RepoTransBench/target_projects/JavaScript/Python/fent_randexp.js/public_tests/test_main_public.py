import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from randexp.randexp import RandExp

def test_randexp_generate_string_matches_regexp():
    re_ = RandExp(r"^A\d{2}Z$")
    for _ in range(10):
        s = re_.gen()
        assert RandExp(r"^A\d{2}Z$").match(s), f'Result "{s}" does not match ^A\\d{{2}}Z$'
        assert s[0] == "A" and s[-1] == "Z"

def test_randexp_generate_digits_with_word_boundaries():
    re_ = RandExp(r"\b\d{3}\b")
    for _ in range(10):
        s = re_.gen()
        assert RandExp(r"\b\d{3}\b").match(s), f'Got "{s}"'
        assert len(s) == 3

def test_randexp_generate_alternative_branches():
    re_ = RandExp(r"cat|bat|rat")
    options = {"cat", "bat", "rat"}
    for _ in range(5):
        s = re_.gen()
        assert s in options