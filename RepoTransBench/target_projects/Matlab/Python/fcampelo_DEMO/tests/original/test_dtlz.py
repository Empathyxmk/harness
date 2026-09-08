import numpy as np
import pytest

from src.dtlz import dtlz6, dtlz7, dtlz_distance, dtlz_range

def test_dtlz6_normal():
    M = 3
    n = (M-1)+10
    mu = 2
    x = np.random.rand(n, mu)
    f = dtlz6(x, M)
    assert f.shape == (M, mu)

def test_dtlz6_error_dim():
    M = 3
    n = (M-1)+10
    mu = 2
    x = np.random.rand(n-1, mu)
    with pytest.raises(ValueError):
        dtlz6(x, M)

def test_dtlz7_normal():
    M = 3
    n = (M-1)+20
    mu = 4
    x = np.random.rand(n, mu)
    f = dtlz7(x, M)
    assert f.shape == (M, mu)

def test_dtlz7_error_dim():
    M = 3
    n = (M-1)+20
    mu = 1
    x = np.random.rand(n-1, mu)
    with pytest.raises(ValueError):
        dtlz7(x, M)

def test_dtlz_distance_all_cases():
    mu = 2
    # dtlz1: k=5, x(last)=0.5
    k = 5
    xopt = np.vstack([np.random.rand(k, mu), 0.5*np.ones((k, mu))])
    d = dtlz_distance(xopt, 'dtlz1')
    assert d.shape == (1, mu)

    # dtlz2, dtlz3, dtlz4, dtlz5, dtlz6, dtlz7
    fnames = ['dtlz2','dtlz3','dtlz4','dtlz5','dtlz6','dtlz7']
    for fname in fnames:
        if fname in ['dtlz2','dtlz3','dtlz4','dtlz5']:
            k = 10
            xlast = 0.5
            n = k
        elif fname == 'dtlz6':
            k = 10
            xlast = 0
            n = k
        elif fname == 'dtlz7':
            k = 20
            xlast = 0
            n = k
        xopt = np.random.rand(n*2, mu)
        xopt[-k:,:] = xlast
        d = dtlz_distance(xopt, fname)
        assert d.shape == (1, mu)

def test_dtlz_range_all_cases():
    M = 3
    for fname in ['dtlz1','dtlz2','dtlz3','dtlz4','dtlz5','dtlz6','dtlz7']:
        lim = dtlz_range(fname, M)
        if fname == 'dtlz1':
            n = (M-1)+5
        elif fname == 'dtlz7':
            n = (M-1)+20
        else:
            n = (M-1)+10
        assert lim.shape == (n, 2)
        assert np.all(lim[:,0] == 0)
        assert np.all(lim[:,1] == 1)

def test_dtlz_range_error():
    with pytest.raises(ValueError):
        dtlz_range('foo', 3)
    with pytest.raises(ValueError):
        dtlz_range('dtlz9', 3)