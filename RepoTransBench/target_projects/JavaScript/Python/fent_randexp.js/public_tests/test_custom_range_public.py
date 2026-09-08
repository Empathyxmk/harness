import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from randexp.randexp import RandExp

def test_randexp_custom_range_pattern():
    re = RandExp(r"[A-M]{4}")
    for _ in range(5):
        s = re.gen()
        assert RandExp(r"[A-M]{4}").match(s), f'Result "{s}" does not match /^[A-M]{{4}}$/'

def test_randexp_custom_range_digit_exclude_zero():
    re = RandExp(r"[1-5]{3}")
    for _ in range(5):
        s = re.gen()
        assert RandExp(r"[1-5]{3}").match(s)

def test_randexp_custom_range_unicode():
    re = RandExp(r"[\u0400-\u0410]{2}")
    for _ in range(5):
        s = re.gen()
        assert len(s) == 2
        assert RandExp(r"[\u0400-\u0410]{2}").match(s), f"Got {s}"