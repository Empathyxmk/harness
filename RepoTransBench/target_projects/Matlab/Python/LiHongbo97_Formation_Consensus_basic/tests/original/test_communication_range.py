import numpy as np
from lihongbo_consensus.helpers import communication_range

def test_communication_range():
    P = np.array([[0, 0], [1, 1], [3, 3]])
    rc = 1.5
    adj = communication_range(P, rc)
    assert adj.shape == (3, 3)
    assert adj[0, 1] in [0, 1]