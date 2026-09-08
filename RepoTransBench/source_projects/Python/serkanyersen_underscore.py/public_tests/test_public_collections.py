import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import underscore

def test_map_public():
    assert underscore.map_([4, 5, 6], lambda x: x + 1) == [5, 6, 7]