import pytest
import types
import os
import glob
import fnmatch
from src.get_value import get_value

def units(get_value_fn):
    # Only a loose simulation, as the JS units runner isn't specified in detail. We'll add basic coverage.
    # Simulate a unit: get_value({'r':{'s':{'t':73}}}, 'r.s.t') == 73
    assert get_value_fn({'r': {'s': {'t': 73}}}, 'r.s.t') == 73
    # with default
    assert get_value_fn({'x': 1}, 'y', {'default': 19}) == 19
    # array path
    assert get_value_fn({'l':[70,80]}, ['l', 1]) == 80
    # Escaped
    assert get_value_fn({'a.b': {'x': 44}}, r'a\.b.x') == 44

def test_units_get_value():
    units(get_value)