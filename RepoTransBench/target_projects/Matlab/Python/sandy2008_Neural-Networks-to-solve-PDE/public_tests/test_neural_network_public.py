import numpy as np
from src.pde_utils.neural_network import neural_network_flexible

def test_neural_network_public_vars():
    w1 = np.array([[0.4, 0.6], [0.2, 0.8], [-0.3, 0.1]])
    b1 = np.array([0.1, 0.2, 0.0])
    w2 = np.array([0.3, 0.7, 0.4])
    b2 = 0.05
    x = np.array([0.6, 0.3])
    a1, y = neural_network_flexible(w1, b1, w2, b2, x)
    assert np.all((a1 > 0) & (a1 < 1))
    assert isinstance(y, (float, np.floating, np.number)) or np.isscalar(y)
    x2 = np.array([0.2, 0.8])
    a2, y2 = neural_network_flexible(w1, b1, w2, b2, x2)
    assert np.all((a2 > 0) & (a2 < 1))
    assert isinstance(y2, (float, np.floating, np.number)) or np.isscalar(y2)