import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import underscore

def test_identity():
    assert underscore.identity(42) == 42