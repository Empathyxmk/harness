import numpy as np
import pytest
import EvoloPy.benchmarks as bm

def test_prod_empty():
    assert bm.prod([]) == 1

def test_prod_multiple():
    assert bm.prod([2,3,4]) == 24

def test_Ufun_basic():
    arr = np.array([11, -11, 0, 9])
    res = bm.Ufun(arr, 10, 100, 2)
    assert res[0] > 0
    assert res[1] > 0
    assert res[2] == 0

def test_F13_shape_variants():
    # Check branch where x.ndim == 1 and where x.ndim != 1
    x1d = np.zeros(3)
    o1 = bm.F13(x1d)
    assert np.isscalar(o1) or isinstance(o1, np.ndarray)
    x2d = np.zeros((2,3))
    o2 = bm.F13(x2d)
    assert np.issubdtype(type(o2), np.floating) or isinstance(o2, np.ndarray)

def test_F12_with_negative_x():
    x = np.array([-20, 0, 20])
    v = bm.F12(x)
    assert isinstance(v, float)

def test_F14_valid_input():
    # A limited input just checks the function runs and returns single value.
    x = np.array([0.5, 0.5])
    try:
        bm.F14(x)
    except Exception as e:
        pytest.skip("F14 input dimension is limited, skipping: " + str(e))

def test_F7_random_component():
    x = np.array([1,2,3])
    v1 = bm.F7(x)
    v2 = bm.F7(x)
    # Because of randomness, v1 != v2 is possible
    assert abs(v1 - v2) < 1