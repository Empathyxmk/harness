import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import underscore

def test_random_public():
    num = underscore.random(20, 25)
    assert (20 <= num <= 25)