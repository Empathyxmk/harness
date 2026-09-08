import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chapter12.stats_list_setup import StatsList

import pytest

@pytest.fixture
def statslist():
    return StatsList([9, 18, 27])

def test_mean_public(statslist):
    assert statslist.mean() == 18.0

def test_max_public(statslist):
    assert max(statslist) == 27

def test_min_public(statslist):
    assert min(statslist) == 9