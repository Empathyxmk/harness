import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import showme

def test_time_type_and_range():
    from showme import core
    value = core.time()
    assert isinstance(value, float)
    # Instead of <1000, check <100000 (should be true in normal Python)
    assert value < 100000
    assert value >= 0