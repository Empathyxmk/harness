import numpy as np
from src.izougend_mcmcda.public_utils import move1_birth, move2_death, move3_split, move4_merge

def test_move1_birth():
    T = 6
    Y = [np.random.randn(3,5) for _ in range(T)]
    W = []
    W2, born = move1_birth(W, T, Y)
    assert isinstance(W2, list) and len(W2) == 1
    assert isinstance(W2[0], np.ndarray) and W2[0].size > 0
    assert born == 1

def test_move2_death():
    T = 6
    Y = [np.random.randn(3,5) for _ in range(T)]
    W = []
    W2, born = move1_birth(W, T, Y)
    W3 = W2
    W4, dead = move2_death(W3, T)
    assert isinstance(W4, list) and len(W4) == 0
    assert dead == 1

def test_move3_split():
    T = 6
    W5 = [np.array([1,2,3]), np.array([4,5,6])]
    W6, did_split = move3_split(W5, T)
    assert isinstance(W6, list)
    assert np.isscalar(did_split)

def test_move4_merge():
    T = 6
    W7 = [np.random.randn(10), np.random.randn(8), np.random.randn(7)]
    W8, did_merge = move4_merge(W7, T)
    assert isinstance(W8, list)