import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import underscore

def test_chunk():
    assert underscore.chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

def test_compact():
    assert underscore.compact([0, 1, False, 2, '', 3]) == [1, 2, 3]