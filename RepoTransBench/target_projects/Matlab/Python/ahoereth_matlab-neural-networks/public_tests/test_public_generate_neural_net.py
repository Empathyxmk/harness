import numpy as np
import pytest

from src.neural_net import generate_neural_net

def test_basic_generation_public():
    layers = [8,6,3]
    neuralNet = generate_neural_net(layers)
    assert len(neuralNet) == len(layers) - 1
    assert neuralNet[0].shape == (layers[0], layers[1])
    assert neuralNet[1].shape == (layers[1], layers[2])
    assert np.all(neuralNet[0] >= -1) and np.all(neuralNet[0] <= 1)
    assert np.all(neuralNet[1] >= -1) and np.all(neuralNet[1] <= 1)

def test_two_layer_network_public():
    layers = [4,2]
    neuralNet = generate_neural_net(layers)
    assert len(neuralNet) == 1
    assert neuralNet[0].shape == (4,2)

def test_zero_or_negative_layer_size_public():
    with pytest.raises(Exception):
        generate_neural_net([4,0,3])
    with pytest.raises(Exception):
        generate_neural_net([2,-1,2])