import numpy as np
from lihongbo_consensus.helpers import detection, find_hop

def test_detection_and_find_hop():
    P = np.array([[0, 0], [3, 4]])
    rc = 5
    A = detection(P, rc)
    assert np.array_equal(A, np.array([[0, 1], [1, 0]]))

    adj = np.array([[0, 1], [1, 0]])
    hop = find_hop(adj, 1, 2)
    assert hop == 1