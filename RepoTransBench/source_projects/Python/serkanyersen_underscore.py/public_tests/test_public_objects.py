import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import underscore

def test_keys_public():
    assert set(underscore.keys({'x': 42, 'y': 100})) == {'x', 'y'}