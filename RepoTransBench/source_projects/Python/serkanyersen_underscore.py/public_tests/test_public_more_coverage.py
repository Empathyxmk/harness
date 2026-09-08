import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + '/..')
from src import underscore

def test_is_empty_public():
    assert underscore.is_empty({}) is True
    assert underscore.is_empty({'a': "z"}) is False