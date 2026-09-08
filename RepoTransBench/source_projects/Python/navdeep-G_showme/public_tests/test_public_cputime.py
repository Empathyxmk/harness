import sys
import os
import pytest

# Add project root to sys.path for showme import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import showme

def test_public_cputime_runs():
    # We can't predict cputime, just ensure it runs and returns a float
    from showme import core
    value = core.cputime()
    assert isinstance(value, float)
    assert value >= 0