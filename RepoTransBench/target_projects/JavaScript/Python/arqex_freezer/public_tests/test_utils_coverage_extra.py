from src import utils

def test_is_array_should_return_false_for_string():
    assert utils.isArray("hello") is False

def test_is_object_should_return_false_for_boolean():
    assert utils.isObject(True) is False

def test_is_function_should_return_false_for_number():
    assert utils.isFunction(123) is False

def test_own_works_for_object_with_undefined_proto_and_different_property():
    obj = dict()
    obj['y'] = 2
    assert utils.own(obj, 'y') is True

def test_equal_detects_non_identical_objects_with_same_key_but_different_value():
    assert utils.equal({'a': 2}, {'a': 3}) is False

def test_equal_detects_arrays_with_same_length_but_different_contents():
    assert utils.equal(['x', 'y'], ['x', 'z']) is False