import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src import underscore

def test_once_public():
    called = []
    def func():
        called.append("called")
        return "foo"
    once_func = underscore.once(func)
    assert once_func() == "foo"
    once_func()
    assert called == ["called"]