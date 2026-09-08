import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import chronological

def test_dummy_add_public():
    assert chronological.dummy_add(8, 4) == 12
    assert chronological.dummy_add(-5, 10) == 5
    assert chronological.dummy_add(7, -7) == 0