import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import underscore

def test_chunk_public():
    assert underscore.chunk([10, 20, 30, 40, 50], 3) == [[10, 20, 30], [40, 50]]

def test_compact_public():
    assert underscore.compact([None, 'hello', '', 0, 9, False, 5]) == ['hello', 9, 5]