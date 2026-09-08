import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from randexp.randexp import RandExp

def gen_max_char(re_obj):
    output = re_obj.gen()
    return max(ord(c) for c in output) if output else 0

def test_modify_range_globally(monkeypatch):
    # Prototype/global range manipulation
    dr = RandExp.defaultRange
    dr.subtract(0, 126)
    dr.add(127, 65535)
    re = RandExp(r".{100}")
    dr.add(0, 126)
    dr.subtract(127, 65535)
    max_char = gen_max_char(re)
    assert max_char >= 127

def test_modify_range_regexp_instance():
    r = RandExp(r"[\d\D]{100}")
    dr = RandExp.defaultRange.clone()
    dr.subtract(0, 126)
    dr.add(127, 65535)
    r.defaultRange = dr
    re = RandExp(r.pattern)
    re.defaultRange = dr
    max_char = gen_max_char(re)
    assert max_char >= 127

def test_modify_range_randexp_instance():
    re = RandExp(r"[\s\S]{100}")
    max_char = gen_max_char(re)
    assert max_char < 127

    re.defaultRange.subtract(0, 126)
    re.defaultRange.add(127, 65535)
    max_char2 = gen_max_char(re)
    assert max_char2 >= 127

def test_modify_range_negated_set():
    re = RandExp(r"[^a]{100}")
    max_char = gen_max_char(re)
    assert max_char < 127

    re.defaultRange.subtract(0, 126)
    re.defaultRange.add(127, 65535)
    max_char2 = gen_max_char(re)
    assert max_char2 >= 127