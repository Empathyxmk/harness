import pytest
from src.mfit_opts import mfit_opts

def test_unrecognized_field_public():
    with pytest.raises(ValueError, match="mfit_opts:invalid_arg"):
        mfit_opts('notafield', 1)

def test_nan_value_public():
    import math
    opts = mfit_opts(display=float('nan'))
    assert isinstance(opts['display'], float) and math.isnan(opts['display'])