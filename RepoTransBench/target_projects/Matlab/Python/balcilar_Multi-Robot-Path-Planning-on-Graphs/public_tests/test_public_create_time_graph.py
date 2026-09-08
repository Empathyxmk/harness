import pytest
import numpy as np
from src.createtimegraph import createtimegraph

def test_public_create_time_graph():
    adj = np.array([
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0]
    ])
    T = 2
    # We don't have edge or loc, call with minimal inputs for the function shape
    # We'll assume edge=[[1,2],[1,3],[2,3],[2,1],[3,1],[3,2]] for adjacency
    edge = np.array([[1,2],[1,3],[2,3],[2,1],[3,1],[3,2]])
    loc = np.array([[0,0], [0,1], [1,1]])
    tgraph, tedge, tloc = createtimegraph(adj, edge, loc, T)
    assert tgraph.shape == (6, 6)
    assert np.all(np.diag(tgraph) == 0)
    assert tgraph[0, 1] == 1
    assert tgraph[3, 4] == 1