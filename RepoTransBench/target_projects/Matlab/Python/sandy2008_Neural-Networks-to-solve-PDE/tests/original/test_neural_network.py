import numpy as np
from src.pde_utils.neural_network import neural_network, sigmoid

def test_neural_network_simple_input():
    num_hidden = 3
    W1_test = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])  # shape (2,3)
    W2_test = np.array([0.7, 0.8, 0.9])  # shape (3,)

    x_input = np.array([0.5, 0.5])  # shape (2,)

    a1_raw = np.dot(x_input, W1_test)  # (3,)
    a1_expected = sigmoid(a1_raw)
    expected_output = np.dot(a1_expected, W2_test)

    actual_output = neural_network(x_input, W1_test, W2_test)
    assert abs(actual_output - expected_output) < 1e-9

def test_neural_network_zero_input():
    num_hidden = 3
    W1_test = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])  # shape (2,3)
    W2_test = np.array([0.7, 0.8, 0.9])  # shape (3,)

    x_zero = np.array([0.0, 0.0])
    a1_zero_raw = np.dot(x_zero, W1_test)
    a1_zero_expected = sigmoid(a1_zero_raw)
    expected_zero_output = np.dot(a1_zero_expected, W2_test) # 0.5 * (0.7+0.8+0.9) = 1.2

    actual_zero_output = neural_network(x_zero, W1_test, W2_test)
    assert abs(actual_zero_output - expected_zero_output) < 1e-9