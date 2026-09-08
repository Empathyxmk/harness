import numpy as np
from src.pde_utils.loss_function_public import loss_function

def test_loss_function_public_case():
    y_pred = np.array([0.5, 1.5, 2.5])
    y_true = np.array([1.0, 1.0, 2.0])
    l = loss_function(y_pred, y_true)
    expected = np.mean((y_pred - y_true) ** 2)
    assert abs(l - expected) < 1e-8