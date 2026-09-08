import numpy as np

def test_cellfun2d():
    # Equivalent to cellfun over a 2x2 cell array of numbers, lambda x: sqrt(x)
    A = np.array([[1, 4], [9, 16]])
    f = np.vectorize(lambda x: np.sqrt(x))
    res = f(A)
    np.testing.assert_allclose(res, [[1, 2], [3, 4]], atol=1e-12)

def test_struct_manip():
    # Simulate struct manipulation/field access with Python dicts or objects
    S = [{'foo': 23, 'bar': 45}, {'foo': 77, 'bar': -9}]
    result = [s['bar'] for s in S]
    assert result == [45, -9]

def test_array_sum():
    arr = np.array([11, 22, 33, 44])
    s = arr.sum()
    assert s == 110

def test_logical_ops():
    arr = np.array([False, True, False, True])
    res = np.any(arr)
    assert res is True
    res2 = np.all(arr)
    assert res2 is False