import numpy as np
import pytest

from src.neural_net import generate_neural_net, train_neural_net_static, apply_neural_net

def test_basic_training_convergence():
    layers = [2,2,1]
    initialNet = generate_neural_net(layers)
    input_data = np.array([[0,0],[0,1],[1,0],[1,1]])
    target_data = np.array([0,0,0,1])
    iterations = 10000
    trainedNet = train_neural_net_static(initialNet, iterations, input_data, target_data)
    final_outputs = []
    for row in input_data:
        out, _ = apply_neural_net(trainedNet, row)
        final_outputs.append(float(out))
    final_outputs = np.array(final_outputs)
    tolerance = 0.1
    assert abs(final_outputs[0] - target_data[0]) < tolerance
    assert abs(final_outputs[1] - target_data[1]) < tolerance
    assert abs(final_outputs[2] - target_data[2]) < tolerance
    assert (final_outputs[3] > target_data[3] - tolerance) and (final_outputs[3] < target_data[3] + tolerance)

def test_zero_iterations():
    layers = [2,2,1]
    initialNet = generate_neural_net(layers)
    input_data = np.array([[0,0]])
    target_data = np.array([0])
    iterations = 0
    trainedNet = train_neural_net_static(initialNet, iterations, input_data, target_data)
    for w0, w1 in zip(initialNet, trainedNet):
        np.testing.assert_allclose(w0, w1)

def test_single_input_output_pair():
    layers = [1,2,1]
    initialNet = generate_neural_net(layers)
    input_data = np.array([[0.5]])
    target_data = np.array([0.8])
    iterations = 5000
    trainedNet = train_neural_net_static(initialNet, iterations, input_data, target_data)
    output, _ = apply_neural_net(trainedNet, input_data[0])
    assert abs(output - target_data[0]) < 0.1

def test_large_input_target_matrices():
    layers = [5,10,3]
    initialNet = generate_neural_net(layers)
    num_samples = 100
    input_data = np.random.rand(num_samples, 5)
    target_data = (np.sum(input_data, axis=1) / 5 > 0.5).astype(float)
    train_neural_net_static(initialNet, 2000, input_data, target_data)
    trainedNet = train_neural_net_static(initialNet, 2000, input_data, target_data)
    output, _ = apply_neural_net(trainedNet, input_data[0])
    assert output.shape == (1,)