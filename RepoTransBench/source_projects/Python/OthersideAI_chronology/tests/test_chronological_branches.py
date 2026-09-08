import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import chronological

def test_dummy_positive():
    assert chronological.dummy_positive(5) is True
    assert chronological.dummy_positive(-3) is False
    assert chronological.dummy_positive(0) is False