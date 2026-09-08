import pytest
import re
from src.jxck_assert import *

def test_throws_assertion_error_correct_properties_falsy_string():
    with pytest.raises(AssertionError) as e:
        ok('', 'should not be falsy!')
    exc = e.value
    assert hasattr(exc, "name") and exc.name == "AssertionError"
    assert hasattr(exc, "message") and exc.message == "should not be falsy!"

def test_throws_with_operator_details_for_equal_using_objects():
    with pytest.raises(AssertionError) as e:
        equal({'x': 1}, {'x': 1}, 'fail eq objects')
    assert e.value.message == 'fail eq objects'

def test_throws_with_operator_details_for_not_equal_using_same_string():
    with pytest.raises(AssertionError) as e:
        notEqual('foo', 'foo', 'fail neq str')
    assert e.value.message == 'fail neq str'

def test_deep_equal_with_different_arrays():
    deepEqual([10, 20], [10, 20])
    with pytest.raises(AssertionError):
        deepEqual([10, 20], [20, 10])

def test_not_deep_equal_with_different_arrays():
    notDeepEqual([3, 4], [4, 3])
    with pytest.raises(AssertionError):
        notDeepEqual([3, 4], [3, 4])

def test_strict_equal_and_not_strict_equal_with_booleans():
    strictEqual(True, True)
    with pytest.raises(AssertionError):
        strictEqual(False, 0)
    notStrictEqual(True, False)
    with pytest.raises(AssertionError):
        notStrictEqual(False, False)

def test_deep_equal_with_nested_arrays_objects():
    deepEqual({'z': [9, {'y': 'x'}]}, {'z': [9, {'y': 'x'}]})
    with pytest.raises(AssertionError):
        deepEqual({'z': [9, {'y': 'x'}]}, {'z': [9, {'y': 'notx'}]})

def test_throws_custom_assertion_error_for_numbers():
    def custom():
        raise AssertionError("bad", 99, 33, ">")
    with pytest.raises(AssertionError):
        custom()

def test_assert_throws_predicate_range_error():
    throws(lambda: (_ for _ in ()).throw(ValueError("out of range")), lambda err: isinstance(err, ValueError))
    with pytest.raises(AssertionError):
        throws(lambda: (_ for _ in ()).throw(Exception("other")), lambda err: isinstance(err, ValueError))

def test_assert_throws_with_re_pattern():
    throws(lambda: (_ for _ in ()).throw(Exception("qwerty")), re.compile("wer"))
    with pytest.raises(AssertionError):
        throws(lambda: (_ for _ in ()).throw(Exception("asdfg")), re.compile("wer"))

def test_assert_does_not_throw_fails_on_type_error():
    with pytest.raises(TypeError):
        doesNotThrow(lambda: (_ for _ in ()).throw(TypeError("bad call")))

def test_assert_ok_throws_when_0():
    with pytest.raises(AssertionError):
        ok(0)

def test_if_error_throws_with_array_object():
    with pytest.raises(AssertionError):
        ifError([1,2,3])
    with pytest.raises(AssertionError):
        ifError({'foo': 'bar'})

def test_if_error_does_not_throw_with_undefined_or_false():
    ifError(None)
    ifError(False)