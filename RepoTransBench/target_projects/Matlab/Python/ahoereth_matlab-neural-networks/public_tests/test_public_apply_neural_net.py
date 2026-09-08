import numpy as np
import pytest

from src.neural_net import generate_neural_net, apply_neural_net

def test_simple_network_application_public():
    layers = [2, 1, 1]
    neuralNet = generate_neural_net(layers)
    neuralNet[0] = np.array([[1.2], [-0.8]])
    neuralNet[1] = np.array([[1.5]])
    input_data = np.array([0.7, 0.3])
    output, values = apply_neural_net(neuralNet, input_data)
    expected_hidden_value = 1. / (1 + np.exp(-(input_data @ neuralNet[0])))
    expected_output_value = 1. / (1 + np.exp(-(expected_hidden_value @ neuralNet[1])))
    assert output.shape == (1,)
    np.testing.assert_allclose(output, expected_output_value, rtol=1e-6)
    assert len(values) == len(layers)
    np.testing.assert_array_equal(values[0], input_data)
    np.testing.assert_allclose(values[1], expected_hidden_value, rtol=1e-6)
    np.testing.assert_allclose(values[2], expected_output_value, rtol=1e-6)

def test_multi_layer_network_application_public():
    layers = [4,3,2,1]
    neuralNet = generate_neural_net(layers)
    neuralNet[0] = 2 * np.ones((4,3))
    neuralNet[1] = -1 * np.ones((3,2))
    neuralNet[2] = 0.5 * np.ones((2,1))
    input_data = np.array([0.2, 0.3, 0.4, 0.5])
    output, values = apply_neural_net(neuralNet, input_data)
    assert output.shape == (1,)
    assert len(values) == len(layers)
    np.testing.assert_array_equal(values[0], input_data)
    for idx in range(1, len(values)):
        assert isinstance(values[idx], np.ndarray)
        assert np.all(values[idx] >= 0) and np.all(values[idx] <= 1)

def test_input_vector_orientation_public():
    layers = [4,2,2]
    neuralNet = generate_neural_net(layers)
    neuralNet[0] = np.random.rand(4,2)
    neuralNet[1] = np.random.rand(2,2)
    input_col = np.array([[0.15],[0.25],[0.35],[0.45]])
    input_row = input_col.reshape(-1)
    output_col, values_col = apply_neural_net(neuralNet, input_col)
    output_row, values_row = apply_neural_net(neuralNet, input_row)
    np.testing.assert_allclose(output_col, output_row)
    for c, r in zip(values_col, values_row):
        np.testing.assert_allclose(c, r)

def test_single_neuron_network_public():
    layers = [1,1]
    neuralNet = generate_neural_net(layers)
    neuralNet[0] = np.array([[-0.7]])
    input_data = np.array([-0.3])
    output, values = apply_neural_net(neuralNet, input_data)
    expected_output = 1. / (1 + np.exp(-(input_data @ neuralNet[0])))
    np.testing.assert_allclose(output, expected_output, rtol=1e-6)
    assert len(values) == len(layers)
    np.testing.assert_array_equal(values[0], input_data)
    np.testing.assert_allclose(values[1], expected_output, rtol=1e-6)