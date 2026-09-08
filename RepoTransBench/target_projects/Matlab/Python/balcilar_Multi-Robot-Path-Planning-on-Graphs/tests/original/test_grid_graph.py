import pytest
import numpy as np
from src.grid_graph import GridGraph

def test_grid_graph_2x2():
    graph, pos_to_node = GridGraph(2, 2)
    expected_nodes = 4
    assert graph.shape == (expected_nodes, expected_nodes)
    # Pos_to_node mapping
    assert pos_to_node[0, 0] == 1
    assert pos_to_node[0, 1] == 2
    assert pos_to_node[1, 0] == 3
    assert pos_to_node[1, 1] == 4

    # Node 1 (1,1): right = 2, down = 3
    assert graph[0, 1] == 1
    assert graph[0, 2] == 1
    assert graph[0, 0] == 0
    assert graph[0, 3] == 0

    # Node 2 (1,2): left = 1, down = 4
    assert graph[1, 0] == 1
    assert graph[1, 3] == 1

    # Node 3 (2,1): up = 1, right = 4
    assert graph[2, 0] == 1
    assert graph[2, 3] == 1

    # Node 4 (2,2): up = 2, left = 3
    assert graph[3, 1] == 1
    assert graph[3, 2] == 1

    # All other edges should be 0; sum == 12 for undirected graph with 6 edges (each edge appears twice)
    assert np.sum(graph) == 12

def test_grid_graph_1x1():
    graph, pos_to_node = GridGraph(1, 1)
    expected_nodes = 1
    assert graph.shape == (expected_nodes, expected_nodes)
    assert pos_to_node[0, 0] == 1
    assert graph[0, 0] == 0
    assert np.sum(graph) == 0

def test_grid_graph_1x3():
    graph, pos_to_node = GridGraph(1, 3)
    expected_nodes = 3
    assert graph.shape == (expected_nodes, expected_nodes)
    assert pos_to_node[0, 0] == 1
    assert pos_to_node[0, 1] == 2
    assert pos_to_node[0, 2] == 3

    assert graph[0, 1] == 1
    assert graph[1, 0] == 1
    assert graph[1, 2] == 1
    assert graph[2, 1] == 1

    assert graph[0, 2] == 0
    assert graph[2, 0] == 0
    assert np.sum(graph) == 4