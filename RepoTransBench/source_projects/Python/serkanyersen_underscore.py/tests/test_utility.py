import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import underscore

def test_random():
    num = underscore.random(1, 10)
    assert (1 <= num <= 10)