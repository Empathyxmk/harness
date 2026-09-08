import numpy as np
from tests.original.genCUEandDUE_helper import genCUEandDUE

def test_public_genCUEandDUE():
    N_CUE_pub = 4
    N_DUE_pub = 3
    R = 2
    cue, tx, rx = genCUEandDUE(N_CUE_pub, N_DUE_pub, R)
    assert cue.shape[0] == N_CUE_pub
    assert tx.shape[1] == N_DUE_pub
    assert rx.shape[1] == N_DUE_pub