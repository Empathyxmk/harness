import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import underscore

def test_map():
    assert underscore.map_([1, 2, 3], lambda x: x * 2) == [2, 4, 6]