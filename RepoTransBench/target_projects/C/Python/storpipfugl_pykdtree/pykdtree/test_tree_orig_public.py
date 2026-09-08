import numpy as np
import pytest

from pykdtree import kdtree

def test_public_orig_basic_query():
    data = np.array([[4, 7], [2, 3], [6, 1]], dtype=np.float32)
    tree = kdtree.KDTree(data)
    dist, idx = tree.query(np.array([[2.1, 3.3]], dtype=np.float32))
    assert idx[0] == 1
    assert dist[0] >= 0

def test_public_orig_repeat_query_points():
    data = np.array([[6., 6.], [8., 8.], [10., 10.]], dtype=np.float64)
    tree = kdtree.KDTree(data)
    query = np.array([[6., 6.], [10., 10.]], dtype=np.float64)
    dist, idx = tree.query(query)
    assert np.all(idx == np.array([0, 2]))
    assert np.all(dist == np.zeros(2))

def test_public_orig_one_point():
    data = np.array([[1., 2.]], dtype=np.float32)
    tree = kdtree.KDTree(data)
    dist, idx = tree.query(np.array([[1., 2.]]).astype(np.float32))
    assert idx[0] == 0
    assert dist[0] == 0

def test_public_orig_k_larger_than_points():
    data = np.array([[1., 2.], [3., 4.]], dtype=np.float32)
    tree = kdtree.KDTree(data)
    q = np.array([[2., 2.]], dtype=np.float32)
    dist, idx = tree.query(q, k=3)
    assert dist.shape == (1, 3)
    assert idx.shape == (1, 3)

def test_public_orig_randomized_shape():
    data = np.random.randint(0, 50, (4, 3)).astype(np.float32)
    tree = kdtree.KDTree(data)
    query = np.random.randint(0, 50, (3, 3)).astype(np.float32)
    dist, idx = tree.query(query)
    assert dist.shape == (3,)
    assert idx.shape == (3,)

def test_public_orig_empty_input_error():
    with pytest.raises(ValueError):
        kdtree.KDTree(np.empty((0, 3), dtype=np.float32))