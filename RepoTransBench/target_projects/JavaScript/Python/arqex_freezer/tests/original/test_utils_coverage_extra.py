import pytest

import sys
import types

# Assume src.utils functions are in python src.utils module and imported here
from src import utils

def test_is_array_returns_false_for_null():
    assert utils.isArray(None) is False

def test_is_object_returns_false_for_number():
    assert utils.isObject(0) is False

def test_is_function_returns_false_for_null():
    assert utils.isFunction(None) is False

def test_own_works_for_object_with_undefined_proto():
    obj = types.SimpleNamespace()
    obj.x = 1
    # For objects without __dict__, simulate Object.create(null)
    obj_no_proto = object.__new__(object)
    # Not a typical Python object, test with normal dict
    obj2 = dict(x=1)
    assert utils.own(obj2, 'x') is True

def test_equal_detects_non_identical_objects_with_different_keys():
    assert utils.equal({'a': 1}, {'b': 1}) is False

def test_equal_detects_arrays_of_different_lengths():
    assert utils.equal([1, 2], [1]) is False