import sys
import os
import pytest

# Add project root to sys.path for showme import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import showme
from showme.core import *

def test_additional_functionality():
    # Use different data than private tests
    assert upper("testing") == "TESTING"
    assert add(101, 21) == 122
    assert subtract(45, 14) == 31
    assert multiply(13, 4) == 52
    assert divide(80, 4) == 20.0
    assert divide(77, 5) == 15.4
    assert add(-5, -2) == -7