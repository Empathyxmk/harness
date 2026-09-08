import numpy as np
import pytest

from pykdtree import kdtree

def test_public_tree_basic_neighbor():
    data = np.array([[0., 1.], [2., 3.], [7., 9.]], dtype=np.float32)
    tree = kdtree.KDTree(data)
    dist, idx = tree.query(np.array([[1.9, 3.]]).astype(np.float32))
    assert idx[0] == 1
    assert dist[0] >= 0

def test_public_tree_identical_queries():
    data = np.array([[3., 4.], [3., 4.]], dtype=np.float64)
    tree = kdtree.KDTree(data)
    query = np.array([[3., 4.], [3., 4.]], dtype=np.float64)
    dist, idx = tree.query(query)
    assert np.all(idx == np.array([0, 0])) or np.all(idx == np.array([1, 1]))
    assert np.all(dist == np.zeros(2))

def test_public_tree_one_neighbor():
    data = np.array([[0., 0.]], dtype=np.float32)
    tree = kdtree.KDTree(data)
    dist, idx = tree.query(np.array([[5., 5.]]).astype(np.float32))
    assert idx[0] == 0
    assert dist[0] >= 0

def test_public_tree_more_k_than_points():
    data = np.array([[5., 5.], [6., 6.]], dtype=np.float32)
    tree = kdtree.KDTree(data)
    q = np.array([[4., 4.]], dtype=np.float32)
    dist, idx = tree.query(q, k=5)
    assert dist.shape == (1, 5)
    assert idx.shape == (1, 5)

def test_public_tree_randomized():
    data = np.random.randint(0, 100, (8, 5)).astype(np.float32)
    tree = kdtree.KDTree(data)
    query = np.random.randint(0, 100, (2, 5)).astype(np.float32)
    dist, idx = tree.query(query)
    assert dist.shape == (2,)
    assert idx.shape == (2,)

def test_public_tree_empty_array_error():
    with pytest.raises(ValueError):
        kdtree.KDTree(np.empty((0, 2), dtype=np.float32))