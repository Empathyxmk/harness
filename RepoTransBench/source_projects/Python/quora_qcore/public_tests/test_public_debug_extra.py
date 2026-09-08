from qcore.debug import function_name
from qcore.asserts import assert_eq

def dummy_func():
    pass

def test_public_function_name():
    assert_eq(function_name(dummy_func), "dummy_func")