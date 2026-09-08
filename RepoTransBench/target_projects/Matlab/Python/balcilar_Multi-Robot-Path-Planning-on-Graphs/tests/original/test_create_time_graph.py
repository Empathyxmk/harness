import pytest
import numpy as np
from src.createtimegraph import createtimegraph

def test_create_time_graph_t1():
    Graph = np.array([[0, 1], [1, 0]])
    edge = np.array([[1, 2], [2, 1]])
    loc = np.array([[10, 10], [20, 20]])
    t = 1

    tgraph, tedge, tloc = createtimegraph(Graph, edge, loc, t)
    expected_tgraph = Graph + np.eye(2, dtype=int)
    expected_tedge = np.vstack((edge, [[1, 1], [2, 2]]))
    expected_tloc = loc

    np.testing.assert_array_equal(tgraph, expected_tgraph)
    np.testing.assert_array_equal(np.sort(tedge, axis=0), np.sort(expected_tedge, axis=0))
    np.testing.assert_array_equal(tloc, expected_tloc)

def test_create_time_graph_t2():
    Graph = np.array([[0, 1], [1, 0]])
    edge = np.array([[1, 2], [2, 1]])
    loc = np.array([[10, 10], [20, 20]])
    t = 2

    tgraph, tedge, tloc = createtimegraph(Graph, edge, loc, t)
    nn = 2
    expected_tgraph = np.zeros((t*nn, t*nn), dtype=int)
    expected_tgraph[0:nn, nn:2*nn] = Graph + np.eye(nn, dtype=int)

    expected_tedge = np.array([
        [1, 2+nn], [2, 1+nn], [1, 1+nn], [2, 2+nn]
    ])
    expected_tloc = np.vstack((loc, loc))

    np.testing.assert_array_equal(tgraph, expected_tgraph)
    # Edge equality as sets: not strictly order, but values
    assert set(tuple(row) for row in tedge) == set(tuple(row) for row in expected_tedge)
    np.testing.assert_array_equal(tloc, expected_tloc)

def test_create_time_graph_empty_graph():
    Graph = np.zeros((0, 0), dtype=int)
    edge = np.array([], dtype=int)
    loc = np.array([], dtype=int)
    t = 2

    tgraph, tedge, tloc = createtimegraph(Graph, edge, loc, t)
    assert tgraph.shape == (0,0)
    assert tedge.size == 0
    assert tloc.size == 0

def test_create_time_graph_larger_graph_t3():
    Graph = np.array([[0,1,0],[1,0,1],[0,1,0]])
    edge = np.array([[1,2],[2,1],[2,3],[3,2]])
    loc = np.array([[1,1],[2,2],[3,3]])
    t = 3

    tgraph, tedge, tloc = createtimegraph(Graph, edge, loc, t)
    nn = 3
    assert tgraph.shape == (t*nn, t*nn)
    expected_block = Graph + np.eye(nn, dtype=int)
    np.testing.assert_array_equal(tgraph[0:nn, nn:2*nn], expected_block)
    np.testing.assert_array_equal(tgraph[nn:2*nn, 2*nn:3*nn], expected_block)
    # Edges
    assert any((tedge == [1, 4]).all(1))
    assert any((tedge == [2, 5]).all(1))
    assert any((tedge == [3, 6]).all(1))
    # Locations:
    assert tloc.shape == (t*nn, loc.shape[1])
    np.testing.assert_array_equal(tloc[0:nn, :], loc)
    np.testing.assert_array_equal(tloc[nn:2*nn, :], loc)
    np.testing.assert_array_equal(tloc[2*nn:3*nn, :], loc)