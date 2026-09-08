import numpy as np
from src.pde_utils.loss_function import loss_function

def test_loss_function_basic_execution():
    num_hidden = 10
    W1_test = np.random.randn(2, num_hidden)
    W2_test = np.random.randn(num_hidden)
    x_test = np.linspace(0, 1, 10)
    y_test = np.linspace(0, 1, 10)
    loss = loss_function(W1_test, W2_test, x_test, y_test)
    assert np.isscalar(loss)
    assert not np.isnan(loss)
    assert not np.isinf(loss)