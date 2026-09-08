import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import chronological

def test_dummy_mul():
    assert chronological.dummy_mul(2, 3) == 6
    assert chronological.dummy_mul(-1, 1) == -1
    assert chronological.dummy_mul(0, 5) == 0