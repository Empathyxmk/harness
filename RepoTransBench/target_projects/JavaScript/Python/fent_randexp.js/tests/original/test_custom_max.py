import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from randexp.randexp import RandExp

def test_modify_max_should_generate_infinite_repetitionals_with_new_max(monkeypatch):
    # Set up max=0
    re = RandExp(r".*")
    re.max = 0
    output = re.gen()
    assert output == ""

    regexp_obj = RandExp(r".*")  # simulate the Regexp case
    regexp_obj.max = 0
    output2 = RandExp.randexp(regexp_obj.pattern)
    assert output2 == ""

    # Mimic static/prototype max set
    monkeypatch.setattr(RandExp, "max", 0)
    re2 = RandExp(r".*")
    output3 = re2.gen()
    assert output3 == ""
    if hasattr(RandExp, "max"):
        delattr(RandExp, "max")