import pytest
from src.jxck_assert import *

def test_throws_assertion_error_with_correct_properties():
    with pytest.raises(AssertionError) as e:
        ok(False, 'fail!')
    exc = e.value
    assert hasattr(exc, "name") and exc.name == "AssertionError"
    assert hasattr(exc, "message") and exc.message == "fail!"

def test_throws_with_operator_details_for_equal():
    with pytest.raises(AssertionError) as e:
        equal(1, 2, 'fail eq')
    assert e.value.message == 'fail eq'

def test_throws_with_operator_details_for_not_equal():
    with pytest.raises(AssertionError) as e:
        notEqual(1, 1, 'fail neq')
    assert e.value.message == 'fail neq'

def test_deep_equal_with_arrays_and_objects():
    deepEqual([1, 2], [1, 2])  # Should pass
    with pytest.raises(AssertionError):
        deepEqual([1, 2], [2, 1])

def test_not_deep_equal_with_arrays_and_objects():
    notDeepEqual([1, 2], [2, 1])  # Should pass
    with pytest.raises(AssertionError):
        notDeepEqual([1, 2], [1, 2])

def test_strict_equal_and_not_strict_equal_with_nan_and_zero():
    import math
    with pytest.raises(AssertionError):
        strictEqual(float('nan'), float('nan'))
    strictEqual(0, -0)  # In Python 0 == -0, so this should not throw
    with pytest.raises(AssertionError):
        notStrictEqual(0, -0)

def test_deep_equal_with_nested_objects():
    deepEqual({'a': {'b': [1, 2]}}, {'a': {'b': [1, 2]}})
    with pytest.raises(AssertionError):
        deepEqual({'a': {'b': [1, 2]}}, {'a': {'b': [2, 1]}})

def test_throws_custom_assertion_error():
    def custom():
        raise AssertionError("oops", 1, 2, "===")
    with pytest.raises(Exception):
        custom()

def test_assert_throws_predicate_function():
    throws(lambda: (_ for _ in ()).throw(TypeError("bad")), lambda err: isinstance(err, TypeError))
    with pytest.raises(AssertionError):
        throws(lambda: (_ for _ in ()).throw(Exception("zzz")), lambda err: isinstance(err, TypeError))

def test_assert_throws_with_regexp():
    throws(lambda: (_ for _ in ()).throw(Exception("abcdef")), re.compile("abc"))
    with pytest.raises(AssertionError):
        throws(lambda: (_ for _ in ()).throw(Exception("xyz")), re.compile("abc"))

def test_assert_does_not_throw_fails_if_throws():
    with pytest.raises(Exception):
        doesNotThrow(lambda: (_ for _ in ()).throw(Exception("fail")))

def test_assert_ok_throws_no_arguments():
    with pytest.raises(Exception):
        ok()  # no args

def test_if_error_throws_with_objects_and_errors():
    with pytest.raises(Exception):
        ifError(Exception())
    with pytest.raises(Exception):
        ifError({'x': 1})

def test_if_error_does_not_throw_with_empty_str_or_zero():
    ifError("")
    ifError(0)