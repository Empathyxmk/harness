import sys
import os
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import EvoloPy.benchmarks as bm

def test_f1_shifted_public():
    f = bm.F1(np.array([4, -3, 5]))
    # Accept int, float or numpy number, allow np.integer since sometimes numpy returns just int types
    assert isinstance(f, (int, float, np.integer, np.floating))
    assert f >= 0

def test_f4_simple_case_public():
    x = np.array([-10, 15, -20, 5, 9])
    res = bm.F4(x)
    assert isinstance(res, (int, float, np.integer, np.floating))

def test_f9_nonzero_input_public():
    x = np.array([2.1, -3.3, 1.8])
    res = bm.F9(x)
    assert isinstance(res, (float, int, np.floating, np.integer))
    assert res > 0