import numpy as np
import pytest

from src.dtlz import dtlz6, dtlz7, dtlz_distance, dtlz_range

def test_public_dtlz6_normal_alt():
    M = 4
    n = (M-1)+8
    mu = 3
    x = np.random.rand(n, mu)
    x[-8:,:] = 0
    f = dtlz6(x, M)
    assert f.shape == (M, mu)

def test_public_dtlz6_error_dim_alt():
    M = 4
    n = (M-1)+8
    mu = 2
    x = np.random.rand(n-2, mu)
    with pytest.raises(ValueError):
        dtlz6(x, M)

def test_public_dtlz7_normal_alt():
    M = 5
    n = (M-1)+16
    mu = 2
    x = np.random.rand(n, mu)
    f = dtlz7(x, M)
    assert f.shape == (M, mu)

def test_public_dtlz7_error_dim_alt():
    M = 5
    n = (M-1)+16
    mu = 2
    x = np.random.rand(n-3, mu)
    with pytest.raises(ValueError):
        dtlz7(x, M)

def test_public_dtlz_distance_variants():
    mu = 3
    k = 6
    xopt = np.vstack([np.random.rand(k, mu), 0.75*np.ones((k, mu))])
    d = dtlz_distance(xopt, 'dtlz1')
    assert d.shape == (1, mu)

    fnames = ['dtlz2','dtlz3','dtlz4','dtlz5','dtlz6','dtlz7']
    for fname in fnames:
        if fname in ['dtlz2','dtlz3','dtlz4','dtlz5']:
            k = 8
            xlast = 0.25
            n = k
        elif fname == 'dtlz6':
            k = 7
            xlast = 1
            n = k
        elif fname == 'dtlz7':
            k = 12
            xlast = 0.7
            n = k
        xopt = np.random.rand(n*2, mu)
        xopt[-k:,:] = xlast
        d = dtlz_distance(xopt, fname)
        assert d.shape == (1, mu)

def test_public_dtlz_range_variants():
    for M in [2,5]:
        for fname in ['dtlz1','dtlz2','dtlz3','dtlz4','dtlz5','dtlz6','dtlz7']:
            lim = dtlz_range(fname, M)
            if fname == 'dtlz1':
                n = (M-1)+3
            elif fname == 'dtlz7':
                n = (M-1)+14
            else:
                n = (M-1)+6
            assert lim.shape == (n,2)
            assert np.all(lim[:,0] == 0)
            assert np.all(lim[:,1] == 1)

def test_public_dtlz_range_error_alt():
    for bogus in ['dtlz10', '', 'random']:
        with pytest.raises(ValueError):
            dtlz_range(bogus, 2)