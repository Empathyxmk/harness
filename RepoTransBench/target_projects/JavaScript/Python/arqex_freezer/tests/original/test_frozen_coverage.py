import pytest

from src import frozen
from src import utils

def test_freeze_arrays():
    frozen_arr = frozen.freeze([1, 2, 3])
    assert utils.isArray(frozen_arr)
    assert frozen_arr[0] == 1

def test_freeze_objects():
    obj = {'a': 1, 'b': {'c': 2}}
    frozen_obj = frozen.freeze(obj)
    assert frozen_obj['a'] == 1

def test_returns_same_primitive():
    x = 42
    assert frozen.freeze(x) == 42

def test_throw_on_cyclic_structures():
    obj = {}
    obj['self'] = obj
    with pytest.raises(Exception):
        frozen.freeze(obj)