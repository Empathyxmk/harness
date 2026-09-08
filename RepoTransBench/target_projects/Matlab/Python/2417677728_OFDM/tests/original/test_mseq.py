import numpy as np
import pytest
from src.mseq import mseq

def test_basic_functionality():
    n = 3
    taps = [1, 3]
    inidata = [1, 1, 1]
    num = 1
    mout = mseq(n, taps, inidata, num)
    assert mout.shape == (1, 7)
    assert np.all(np.isin(mout, [0, 1]))

def test_multiple_sequences():
    n = 3
    taps = [1, 3]
    inidata = [1, 1, 1]
    num = 2
    mout = mseq(n, taps, inidata, num)
    assert mout.shape == (2, 7)

def test_edge_case_single_bit():
    n = 1
    taps = [1]
    inidata = [1]
    num = 1
    mout = mseq(n, taps, inidata, num)
    assert mout == 1

def test_empty_sequence():
    n = 2
    taps = [1, 2]
    inidata = [0, 0]
    num = 1
    mout = mseq(n, taps, inidata, num)
    mout_flat = np.array(mout).flatten()
    assert np.all(np.isin(mout_flat, [0]))