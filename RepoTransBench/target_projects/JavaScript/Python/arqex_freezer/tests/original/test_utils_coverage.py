import pytest

from src import utils

def test_is_array_returns_true_for_arrays():
    assert utils.isArray([]) is True

def test_is_array_returns_false_for_nonarrays():
    assert utils.isArray({}) is False
    assert utils.isArray('a') is False
    assert utils.isArray(None) is False

def test_is_object_returns_true_for_objects():
    assert utils.isObject({}) is True

def test_is_object_returns_false_for_non_objects():
    assert utils.isObject(None) is False
    assert utils.isObject([]) is False
    assert utils.isObject(lambda: None) is False

def test_is_function_returns_true_for_function():
    assert utils.isFunction(lambda: None) is True

def test_is_function_returns_false_for_non_function():
    assert utils.isFunction(1) is False
    assert utils.isFunction({}) is False

def test_own_acts_like_hasownproperty():
    obj = {'a': 1}
    assert utils.own(obj, 'a') is True
    assert utils.own(obj, 'b') is False

def test_equal_checks_primitives():
    assert utils.equal(1, 1) is True
    assert utils.equal(1, 2) is False

def test_equal_compares_arrays():
    assert utils.equal([1, 2], [1, 2]) is True
    assert utils.equal([1], [1, 2]) is False

def test_equal_compares_objects():
    assert utils.equal({'a': 1}, {'a': 1}) is True
    assert utils.equal({'a': 1}, {'a': 2}) is False
    assert utils.equal({'a': 1}, {'a': 1, 'b': 2}) is False

def test_equal_compares_null_and_none():
    assert utils.equal(None, None) is True
    assert utils.equal(None, None) is True
    assert utils.equal(None, "undefined") is False  # Python: no undefined, so test with a string