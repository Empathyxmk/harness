import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import chronological

def test_dummy_add():
    assert chronological.dummy_add(2, 3) == 5
    assert chronological.dummy_add(-1, 1) == 0
    assert chronological.dummy_add(0, 0) == 0