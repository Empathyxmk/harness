import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from randexp.randexp import RandExp

def test_randexp_maximum_repetitions_no_more_than_custom_max(monkeypatch):
    monkeypatch.setattr(RandExp, "max", 2)
    re = RandExp(r"z{2,}")
    for _ in range(10):
        res = re.gen()
        assert 2 <= len(res) <= 2, f"Result length should be between 2 and 2, got {len(res)}"
        assert re.match(res)
    monkeypatch.setattr(RandExp, "max", 100)

def test_randexp_maximum_repetitions_apply_max_character_classes(monkeypatch):
    monkeypatch.setattr(RandExp, "max", 4)
    re = RandExp(r"[ab]{3,}")
    for _ in range(5):
        res = re.gen()
        assert 3 <= len(res) <= 4
        assert re.match(res)
    monkeypatch.setattr(RandExp, "max", 100)