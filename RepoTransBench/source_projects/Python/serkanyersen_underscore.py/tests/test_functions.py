import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import underscore

def test_once():
    called = []

    def func():
        called.append(1)
        return 3

    once_func = underscore.once(func)
    assert once_func() == 3
    once_func()
    assert called == [1]