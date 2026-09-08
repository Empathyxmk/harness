import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from randexp.randexp import RandExp

import re

from .test_tests import TESTS_DICT

def match(regexp, s, bad):
    err = f"Generated string '{s}' " + ("matches" if bad else "does not match") + f" regexp '{regexp.pattern}'"
    t = regexp.match(s) is not None
    assert bad != t, err

@pytest.mark.parametrize("type_name,type_tests", TESTS_DICT.items())
def test_types(type_name, type_tests):
    for row, t in type_tests.items():
        regs = t['regexp']
        if not isinstance(regs, list):
            regs = [regs]
        for regpat in regs:
            reg = re.compile(regpat)
            rand = RandExp(regpat)
            for _ in range(5):
                match(reg, rand.gen(), t.get('bad', False))
                match(reg, RandExp.randexp(regpat), t.get('bad', False))


def test_call_with_string():
    r = RandExp(r"\d{4}")
    assert len(r.gen()) == 4

def test_with_options():
    r = RandExp(r"hello", "i")
    assert r.ignore_case
    assert not r.multiline

def test_call_shorthand_randexp_method_with_a_string():
    r = RandExp.randexp(r"\d{4}")
    assert len(r) == 4

def test_call_without_string_or_regex():
    with pytest.raises(Exception, match="Expected a regexp or string"):
        r = RandExp({})
        r.gen()

def test_followed_by_groups():
    assert RandExp.randexp(r"hi(?= no one)") == "hi"
    assert RandExp.randexp(r"hi(?! no one)") == "hi"