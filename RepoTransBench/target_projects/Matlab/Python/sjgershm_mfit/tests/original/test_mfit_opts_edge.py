import pytest
from src.mfit_opts import mfit_opts

def test_add_new_field_to_opts():
    custom = {'M': 50, 'sd':7, 'customfield': 42}
    opts = mfit_opts(custom)
    assert opts['customfield'] == 42

def test_input_is_struct_with_all_fields():
    inopts = dict(M=1, vectorize=0, hierarchical=0, sd=0.5, nStarts=10)
    opts = mfit_opts(inopts)
    assert opts == inopts