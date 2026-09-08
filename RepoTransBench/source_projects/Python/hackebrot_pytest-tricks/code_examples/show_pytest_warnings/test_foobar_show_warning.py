# Separate file to avoid base name collision for pytest discovery

import warnings
import pytest

def test_warns():
    with pytest.warns(UserWarning):
        warnings.warn("this is a warning", UserWarning)