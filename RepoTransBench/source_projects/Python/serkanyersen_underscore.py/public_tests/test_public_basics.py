import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import underscore

def test_identity_public():
    assert underscore.identity("underscore") == "underscore"