import numpy as np
from lihongbo_consensus.helpers import find_hop

def test_public_detection_and_find_hop():
    obj_p = np.array([1, 1])
    obs_p = np.array([[0, 2], [2, 1]])
    dists = np.sqrt(np.sum((obs_p - obj_p)**2, axis=1))
    assert np.all(dists > 0)

    adj = np.array([[0, 1, 0],
                    [1, 0, 1],
                    [0, 1, 0]])
    visited = np.array([1, 0, 0])
    hops = find_hop(adj, visited)
    assert hops.shape == (3,)