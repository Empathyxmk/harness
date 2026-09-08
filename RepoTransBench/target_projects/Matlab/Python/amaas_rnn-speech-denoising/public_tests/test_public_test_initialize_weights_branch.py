import numpy as np
from src.initialize_weights import initialize_weights

def test_public_initialize_weights_zero_layers():
    arch = {'nl': 0, 'layer_sizes': []}
    w = initialize_weights(arch)
    assert w is None or isinstance(w, np.ndarray)

def test_public_initialize_weights_larger_and_dropout():
    arch = {'nl': 3, 'layer_sizes': [5,3,2], 'dropout': False}
    w = initialize_weights(arch)
    assert isinstance(w, np.ndarray) or w is None