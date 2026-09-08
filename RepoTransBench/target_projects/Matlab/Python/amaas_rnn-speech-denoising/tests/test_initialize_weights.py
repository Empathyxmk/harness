import numpy as np
from src.initialize_weights import initialize_weights

def test_initialize_weights_basic():
    d1, d2 = 5, 3
    W = initialize_weights(d1, d2)
    assert W.shape == (d1, d2)
    assert np.all(W < 0.1) and np.all(W > -0.1)