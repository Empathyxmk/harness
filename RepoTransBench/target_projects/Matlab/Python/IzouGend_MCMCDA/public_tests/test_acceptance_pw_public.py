import numpy as np
from src.izougend_mcmcda.public_utils import acceptance_pw_public

def test_acceptance_pw_public_basic():
    w1 = [1, 5, 3]
    w2 = [3, 1, 8]
    beta = 0.8
    ratio = acceptance_pw_public(w1, w2, beta)
    assert 0 <= ratio <= 1

def test_acceptance_pw_public_alternate():
    w1 = [10, 10, 10, 10]
    w2 = [6, 7, 8, 9]
    beta = 1.2
    ratio = acceptance_pw_public(w1, w2, beta)
    assert 0 <= ratio <= 1