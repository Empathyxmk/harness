import pytest
import numpy as np
from src.initialize_weights import initialize_weights

def test_initialize_weights_invalid_architecture():
    arch = {'nl': 1, 'layer_sizes': []}
    w = initialize_weights(arch)
    assert w is None or isinstance(w, np.ndarray)

def test_initialize_weights_with_dropout():
    arch = {'nl': 2, 'layer_sizes': [2,2], 'dropout': True}
    w = initialize_weights(arch)
    assert isinstance(w, np.ndarray) or w is None