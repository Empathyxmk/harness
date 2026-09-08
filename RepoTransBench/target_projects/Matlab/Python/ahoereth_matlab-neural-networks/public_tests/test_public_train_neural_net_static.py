import numpy as np

from src.neural_net import generate_neural_net, train_neural_net_static, apply_neural_net

def test_static_network_public():
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    Y = np.array([0, 1, 1, 1])
    neuralNet = generate_neural_net([2,3,1])
    trainedNet, losses = train_neural_net_static(neuralNet, X, Y, learning_rate=0.3, epochs=40, return_losses=True)
    assert losses[-1] < 1.0
    assert losses[-1] < losses[0]
    preds = []
    for i in range(X.shape[0]):
        o, _ = apply_neural_net(trainedNet, X[i])
        preds.append(o > 0.5)
    acc = np.sum(np.array(preds) == Y) / Y.size
    assert acc >= 0.75

def test_static_network_small_batch_public():
    X = np.array([[0],[1]])
    Y = np.array([1,0])
    neuralNet = generate_neural_net([1,1])
    trainedNet, losses = train_neural_net_static(neuralNet, X, Y, learning_rate=0.15, epochs=25, batch_size=1, return_losses=True)
    assert losses[-1] < losses[0]
    preds = []
    for i in range(X.shape[0]):
        o, _ = apply_neural_net(trainedNet, X[i])
        preds.append(o > 0.5)
    acc = np.sum(np.array(preds).reshape(-1) == Y) / Y.size
    assert acc >= 0.5