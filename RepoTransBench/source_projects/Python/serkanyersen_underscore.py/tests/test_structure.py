import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import underscore

def test_pairs():
    assert underscore.pairs({'a': 1, 'b': 2}) == [('a', 1), ('b', 2)]