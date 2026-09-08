import pytest
from msckf_mono.corner_detector import CornerDetector

def test_construct_destruct():
    cd1 = CornerDetector()
    # Destroyed at end of scope (noop in Python)

def test_multiple_construct_destruct():
    for _ in range(7):
        cd2 = CornerDetector()
        # Destroyed at end of loop

def test_allocation_pointer_not_null():
    cd3 = CornerDetector()
    assert cd3 is not None
    cd4 = CornerDetector()
    assert cd4 is not None
    del cd3
    del cd4