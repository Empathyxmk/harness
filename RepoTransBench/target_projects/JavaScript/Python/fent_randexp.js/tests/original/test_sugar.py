import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from randexp.randexp import RandExp

def test_sugar_global(monkeypatch):
    # Assume sugar() monkey-patches re objects in user implementation
    RandExp.sugar()
    regexp = RandExp(r".ff something+")
    assert callable(regexp.gen)
    assert regexp.match(regexp.gen())
    assert regexp.match(regexp.gen())

    regexp.max = 0
    assert regexp.gen()[4:] == "something"