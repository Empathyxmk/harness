import pytest
from src.mfit_opts import mfit_opts

def test_default_fields():
    opts = mfit_opts()
    assert 'method' in opts
    assert 'display' in opts

def test_invalid_method_public():
    with pytest.raises(ValueError, match="mfit_opts:invalid_arg"):
        mfit_opts(method=123)

def test_set_fields_public():
    opts = mfit_opts(display=0, maxiter=300)
    assert opts['display'] == 0
    assert opts['maxiter'] == 300