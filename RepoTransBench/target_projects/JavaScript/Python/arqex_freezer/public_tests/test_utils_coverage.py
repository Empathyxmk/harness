from src import utils

def test_is_array_detects_array_public():
    assert utils.isArray([10, 20]) is True
    assert utils.isArray({'k': 1}) is False

def test_is_object_detects_objects_and_not_array_public():
    assert utils.isObject({'b': 2}) is True
    assert utils.isObject([]) is False

def test_is_function_detects_function_and_not_string_public():
    def func():
        pass
    assert utils.isFunction(func) is True
    assert utils.isFunction('not a func') is False

def test_own_properly_detects_own_and_prototype_properties_public():
    class C:
        def __init__(self):
            self.a = 9
        b = 12
    obj = C()
    assert utils.own(obj.__dict__, "a") is True
    assert utils.own(obj.__dict__, "b") is False

def test_equal_returns_true_for_same_value_primitives_public():
    assert utils.equal("foo", "foo") is True

def test_equal_returns_false_for_different_length_arrays_public():
    assert utils.equal([1, 2, 3], [1, 2]) is False