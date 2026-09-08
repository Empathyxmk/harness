import pytest
from msckf_mono.corner_detector import CornerDetector


def test_constructor_destructor():
    detector = CornerDetector()
    # Implicit __del__ on function end; nothing to assert

def test_repeated_construction():
    for _ in range(5):
        detector = CornerDetector()
        # Implicit __del__ on function end

def test_pointer_allocation():
    detector = CornerDetector()
    assert detector is not None
    # delete not required, but remove binding explicitly for symmetry
    del detector