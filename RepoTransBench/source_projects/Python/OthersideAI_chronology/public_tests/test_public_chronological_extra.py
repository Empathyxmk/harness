import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import chronological

def test_dummy_mul_public():
    assert chronological.dummy_mul(4, 5) == 20
    assert chronological.dummy_mul(-2, 6) == -12
    assert chronological.dummy_mul(0, -3) == 0