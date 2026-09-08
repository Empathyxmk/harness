from src.mfit_opts import mfit_opts

def test_default_opts():
    opts = mfit_opts()
    assert opts['M'] == 10000
    assert opts['vectorize'] == 1
    assert opts['hierarchical'] == 1
    assert opts['sd'] == 1
    assert opts['nStarts'] == 2

def test_partial_opts():
    inopts = dict(M=5, sd=3)
    opts = mfit_opts(inopts)
    assert opts['M'] == 5
    assert opts['vectorize'] == 1
    assert opts['hierarchical'] == 1
    assert opts['sd'] == 3
    assert opts['nStarts'] == 2

def test_empty_opts():
    opts = mfit_opts([])
    assert opts['M'] == 10000
    assert opts['vectorize'] == 1
    assert opts['hierarchical'] == 1
    assert opts['sd'] == 1
    assert opts['nStarts'] == 2