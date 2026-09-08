import numpy as np

from src.neural_net import generate_neural_net, train_neural_net, apply_neural_net

def test_training_converges_public():
    X = np.array([[0,1],[1,0],[1,1],[0,0]])
    Y = np.array([1,1,0,0])
    neuralNet = generate_neural_net([2,3,1])
    trainedNet, losses = train_neural_net(neuralNet, X, Y, learning_rate=0.8, epochs=75, batch_size=2, return_losses=True)
    assert losses[-1] < losses[0]
    preds = []
    for i in range(X.shape[0]):
        o, _ = apply_neural_net(trainedNet, X[i])
        preds.append(o > 0.5)
    acc = np.sum(np.array(preds).reshape(-1) == Y) / Y.size
    assert acc >= 0.75

def test_different_architecture_train_public():
    X = np.array([[1,0,0], [0,1,0], [0,0,1], [1,1,1]])
    Y = np.array([1,1,0,0])
    neuralNet = generate_neural_net([3,2,2,1])
    trainedNet, losses = train_neural_net(neuralNet, X, Y, learning_rate=0.5, epochs=30, return_losses=True)
    assert losses[-1] < losses[0]
    preds = []
    for i in range(X.shape[0]):
        o, _ = apply_neural_net(trainedNet, X[i])
        preds.append(o > 0.5)
    acc = np.sum(np.array(preds).reshape(-1) == Y) / Y.size
    assert acc >= 0.5