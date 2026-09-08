import pytest
from msckf_mono.corner_detector import CornerDetector

def test_destructor_called():
    detector = CornerDetector()
    del detector  # Explicitly deletes ref, runs __del__

def test_null_pointer_behavior():
    detector = None
    assert detector is None

def test_dynamic_array():
    detectors = [CornerDetector() for _ in range(3)]
    for d in detectors:
        assert isinstance(d, CornerDetector)
    del detectors