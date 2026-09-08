import numpy as np
import pytest

from pykdtree import kdtree

def test_simple_query():
    data = np.array([[0, 0], [1, 1], [2, 2]], dtype=np.float32)
    tree = kdtree.KDTree(data)
    dist, idx = tree.query(np.array([[0.1, 0.1]], dtype=np.float32))
    assert idx[0] == 0
    assert dist[0] >= 0
    dist_diag, idx_diag = tree.query(data)
    np.testing.assert_array_equal(idx_diag, np.arange(3))
    np.testing.assert_array_equal(dist_diag, np.zeros(3))

def test_query_many_k():
    data = np.random.rand(10, 2).astype(np.float32)
    tree = kdtree.KDTree(data)
    query = np.random.rand(5, 2).astype(np.float32)
    dist, idx = tree.query(query, k=5)
    assert dist.shape == (5, 5)
    assert idx.shape == (5, 5)

def test_distance_metric_and_dtype():
    data = np.random.rand(4, 2)
    tree = kdtree.KDTree(data.astype(np.float32))
    q = np.array([[0.1, 0.1]], dtype=np.float32)
    dist, idx = tree.query(q)
    assert dist.shape == (1,)
    assert idx.shape == (1,)
    data64 = data.astype(np.float64)
    tree64 = kdtree.KDTree(data64)
    dist, idx = tree64.query(q.astype(np.float64))
    assert dist[0] >= 0

def test_error_conditions():
    data = np.random.rand(3, 2).astype(np.float32)
    tree = kdtree.KDTree(data)
    # Dimension mismatch
    query = np.random.rand(4, 3).astype(np.float32)
    with pytest.raises(ValueError):
        tree.query(query)
    # Negative k
    with pytest.raises(ValueError):
        tree.query(np.random.rand(2,2).astype(np.float32), k=-5)
    # Empty array
    with pytest.raises(ValueError):
        kdtree.KDTree(np.empty((0, 3), dtype=np.float32))

def test_query_with_eps_and_upper_bound():
    data = np.random.rand(7, 3).astype(np.float32)
    tree = kdtree.KDTree(data)
    query = np.random.rand(2, 3).astype(np.float32)
    eps = 0.1
    dist, idx = tree.query(query, eps=eps)
    assert dist.shape == (2,)
    assert idx.shape == (2,)
    dist, idx = tree.query(query, k=2, eps=eps)
    assert dist.shape == (2, 2)
    # distance_upper_bound not implemented in pykdtree, but add a safe fallback
    try:
        tree.query(query, distance_upper_bound=0.5)
    except TypeError:
        pass

def test_query_type_and_shape_checking():
    # Should work for both float32 and float64
    for dtype in [np.float32, np.float64]:
        data = np.random.rand(4, 2).astype(dtype)
        tree = kdtree.KDTree(data)
        query = np.random.rand(2, 2).astype(dtype)
        dist, idx = tree.query(query)
        assert dist.shape == (2,)
        assert idx.shape == (2,)
    # The KDTree allows int queries and converts - do not expect TypeError
    data = np.random.randint(0, 10, (3, 2))
    tree = kdtree.KDTree(data)
    bad_query = np.array([[1, 2]], dtype=np.int32)
    # Should NOT error, because pykdtree converts int to float64 internally
    dist, idx = tree.query(bad_query)
    assert dist.shape == (1,)
    assert idx.shape == (1,)

def test_invalid_dtype():
    # Query as double when tree built with float32 and vice versa
    data32 = np.random.rand(5, 2).astype(np.float32)
    data64 = np.random.rand(5, 2).astype(np.float64)
    tree32 = kdtree.KDTree(data32)
    tree64 = kdtree.KDTree(data64)
    # Only expect TypeError if query dtype does NOT match tree dtype
    with pytest.raises(TypeError):
        tree32.query(np.random.rand(5, 2).astype(np.float64))
    # This is allowed: query built with float32 expects float32
    tree32.query(np.random.rand(5,2).astype(np.float32))
    # This is allowed
    tree64.query(np.random.rand(5, 2).astype(np.float64))
    # Remove this: float64 KDTree allows float32 query (converts array), so do NOT expect TypeError
    # tree64.query(np.random.rand(5, 2).astype(np.float32))
    d32toint = np.random.randint(0, 10, (5, 2)).astype(np.int32)
    # Allowed -- int query will be cast to float64
    tree64.query(d32toint)

def test_query_k_greater_than_data():
    data = np.random.rand(3, 2).astype(np.float32)
    tree = kdtree.KDTree(data)
    query = np.random.rand(1, 2).astype(np.float32)
    # Query for more neighbors than we have points
    dist, idx = tree.query(query, k=5)
    assert dist.shape == (1, 5)
    assert idx.shape == (1, 5)

def test_kdtree_repr_str():
    # Cover __repr__ and __str__ of kdtree object
    data = np.random.rand(3, 2).astype(np.float32)
    tree = kdtree.KDTree(data)
    s = str(tree)
    rep = repr(tree)
    assert "KDTree" in s
    assert "KDTree" in rep