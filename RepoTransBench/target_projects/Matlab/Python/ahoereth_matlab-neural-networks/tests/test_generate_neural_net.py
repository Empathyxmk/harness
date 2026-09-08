import numpy as np
import pytest

from src.neural_net import generate_neural_net

def test_basic_generation():
    layers = [10, 5, 2]
    neuralNet = generate_neural_net(layers)
    assert len(neuralNet) == len(layers)-1
    assert neuralNet[0].shape == (layers[0], layers[1])
    assert neuralNet[1].shape == (layers[1], layers[2])
    assert np.all(neuralNet[0] >= -1) and np.all(neuralNet[0] <= 1)
    assert np.all(neuralNet[1] >= -1) and np.all(neuralNet[1] <= 1)

def test_two_layer_network():
    layers = [3,1]
    nn = generate_neural_net(layers)
    assert len(nn) == 1
    assert nn[0].shape == (3,1)

def test_large_network():
    layers = [100, 50, 25, 10, 5, 1]
    nn = generate_neural_net(layers)
    assert len(nn) == len(layers)-1
    for i in range(len(layers)-1):
        assert nn[i].shape == (layers[i], layers[i+1])

def test_single_layer_input():
    layers = [5]
    nn = generate_neural_net(layers)
    assert nn == []

def test_empty_layers_input():
    layers = []
    nn = generate_neural_net(layers)
    assert nn == []