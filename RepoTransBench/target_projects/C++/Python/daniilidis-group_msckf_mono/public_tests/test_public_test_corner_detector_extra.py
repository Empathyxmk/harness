import pytest
from msckf_mono.corner_detector import CornerDetector

def test_destructor_via_delete():
    cd = CornerDetector()
    del cd  # Explicitly deletes ref, runs __del__

def test_explicit_null_is_null():
    cd = None
    assert not (cd is not None)

def test_dynamic_array_different_size():
    arr = [CornerDetector() for _ in range(4)]
    for item in arr:
        assert isinstance(item, CornerDetector)
    del arr