import sys
import os
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lafan1 import benchmarks

def test_fast_npss_simple_public():
    # Use an input where NPSS returns a valid float and no weights are all zero
    # Use a linear ramp vs. another ramp offset by +1
    A = np.linspace(1, 2, 24).reshape(2, 12, 1)
    B = np.linspace(2, 3, 24).reshape(2, 12, 1)
    score = benchmarks.fast_npss(A, B)
    assert not np.isnan(score)
    assert isinstance(score, float)

def test_fast_npss_different_nan_guard_public():
    # Slightly different, still valid: another kind of ramp
    A = np.linspace(0, 3, 24).reshape(2, 12, 1)
    B = np.linspace(1, 4, 24).reshape(2, 12, 1)
    score = benchmarks.fast_npss(A, B)
    assert not np.isnan(score)

import pytest
@pytest.mark.skip(reason="Testing skip for public test coverage symmetry")
def test_dummy_skip_public():
    assert True