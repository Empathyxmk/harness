import pytest
from src.grid_graph import GridGraph

def test_public_grid_graph():
    n = 3
    m = 2
    A, xy = GridGraph(n, m)
    assert A.shape == (n*m, n*m)
    assert xy.shape == (n*m, 2)
    row = 0
    assert A[row, :].sum() == 2