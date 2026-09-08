import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import underscore

def test_pairs_public():
    assert underscore.pairs({'foo': 7, 'bar': 8}) == [('foo', 7), ('bar', 8)]