import numpy as np
from src.mseq import mseq

def test_basic_functionality():
    n = 4
    taps = [1, 4]
    inidata = [1, 0, 1, 1]
    num = 1
    mout = mseq(n, taps, inidata, num)
    assert mout.shape == (1, 15)
    assert np.all(np.isin(mout, [0, 1]))

def test_multiple_sequences():
    n = 2
    taps = [1, 2]
    inidata = [1, 0]
    num = 3
    mout = mseq(n, taps, inidata, num)
    assert mout.shape == (3, 3)

def test_edge_case_single_bit():
    n = 1
    taps = [1]
    inidata = [0]
    num = 1
    mout = mseq(n, taps, inidata, num)
    assert mout == 0

def test_empty_sequence():
    n = 2
    taps = [2]
    inidata = [0, 0]
    num = 2
    mout = mseq(n, taps, inidata, num)
    mout = np.array(mout)
    assert np.all(mout == 0)