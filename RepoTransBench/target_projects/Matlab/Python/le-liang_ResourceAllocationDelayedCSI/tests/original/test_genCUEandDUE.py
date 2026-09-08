import numpy as np
from tests.original.genCUEandDUE_helper import genCUEandDUE

def test_genCUEandDUE_basic():
    cue, tx, rx = genCUEandDUE(2, 3, 10, 2, 6, 1)
    assert cue.shape == (2, 2)
    assert tx.shape == (2, 3)
    assert rx.shape == (2, 3)
    # d_min should apply (rx not equal tx)
    assert np.all(np.sqrt(np.sum((rx-tx)**2, axis=0)) >= 1)