import numpy as np
from lihongbo_consensus.helpers import communication_range

def test_public_communication_range():
    pos = np.array([[1, 2], [4, 6], [8, 9]])
    range_ = 5
    adj = communication_range(pos, range_)
    # For 3 points, check it's symmetric and diagonal is zero
    assert np.array_equal(adj, adj.T)
    assert np.all(np.diag(adj) == 0)