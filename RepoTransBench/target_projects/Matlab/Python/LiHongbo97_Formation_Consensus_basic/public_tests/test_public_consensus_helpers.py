import numpy as np

def test_public_consensus_helpers_deg():
    A = np.array([[0, 2, 0], [2, 0, 3], [0, 3, 0]])
    expected_deg = np.array([2, 5, 3])
    deg = np.sum(A, axis=1)
    assert np.array_equal(deg, expected_deg)

def test_public_consensus_helpers_edges():
    A = np.array([[0, 2, 0], [2, 0, 3], [0, 3, 0]])
    edge_idxs = np.where(A)
    assert edge_idxs[0].size > 0