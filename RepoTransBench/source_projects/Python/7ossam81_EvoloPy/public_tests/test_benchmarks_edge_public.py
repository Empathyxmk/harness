import sys
import os
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import EvoloPy.benchmarks as bm

def test_f6_large_value_public():
    # Test with numpy array as input (required by EvoloPy.benchmarks)
    arr = np.array([101])
    f = bm.F6(arr)
    assert isinstance(f, float)
    assert f >= 0

def test_f8_boundary_case_public():
    # Test F8 function on a negative boundary, numpy array input
    x = np.array([-2.5, -2.5, -2.5], dtype=float)
    res = bm.F8(x)
    assert type(res) in (float, np.float64, np.float32)
    assert res >= 0

def test_f10_zero_input_public():
    arr = np.zeros(4)
    result = bm.F10(arr)
    assert abs(result) < 1e-6