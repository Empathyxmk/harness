import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + '/..')
from src import underscore

def test_is_empty():
    assert underscore.is_empty([]) is True
    assert underscore.is_empty([1]) is False