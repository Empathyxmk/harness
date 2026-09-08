import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import jsons

def test_tuple_dump_public():
    t = (11, "world", 3.5)
    dumped = jsons.dump(t)
    assert dumped == [11, "world", 3.5]

def test_tuple_load_public():
    data = [42, "foo", 1.25]
    loaded = jsons.load(data, tuple)
    assert loaded == (42, "foo", 1.25)