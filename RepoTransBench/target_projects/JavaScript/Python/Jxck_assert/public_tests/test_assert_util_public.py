import pytest
from src.jxck_assert import *

def test_assert_ok_truthy_public():
    ok('nonempty')
    ok(42)

def test_assert_ok_falsy_throws_public():
    with pytest.raises(AssertionError):
        ok(None)
    with pytest.raises(AssertionError):
        ok(None)

def test_assert_equal_public():
    equal('abc', 'abc')
    equal('5', 5)
    with pytest.raises(AssertionError):
        equal('foo', 'bar')

def test_assert_not_equal_public():
    notEqual('dog', 'cat')
    with pytest.raises(AssertionError):
        notEqual('abc', 'abc')

def test_assert_deep_equal_public():
    deepEqual({'m':{'n':9}}, {'m':{'n':9}})
    with pytest.raises(AssertionError):
        deepEqual({'a':2}, {'a':3})

def test_assert_not_deep_equal_public():
    notDeepEqual({'p':1}, {'p':2})
    with pytest.raises(AssertionError):
        notDeepEqual({'p':2}, {'p':2})

def test_assert_strict_equal_and_not_strict_equal_public():
    strictEqual('hi', 'hi')
    with pytest.raises(AssertionError):
        strictEqual(2, '2')
    notStrictEqual(11, 22)
    with pytest.raises(AssertionError):
        notStrictEqual(22, 22)

def test_assert_throws_public():
    throws(lambda: (_ for _ in ()).throw(TypeError("err")))
    with pytest.raises(AssertionError):
        throws(lambda: None)

def test_assert_does_not_throw_public():
    doesNotThrow(lambda: 1+1)
    with pytest.raises(Exception):
        doesNotThrow(lambda: (_ for _ in ()).throw(Exception("fail")))

def test_if_error_public():
    ifError(False)
    ifError(0)
    ifError("")
    with pytest.raises(AssertionError):
        ifError(Exception("kaboom"))

def test_assert_ok_with_custom_message_public():
    with pytest.raises(AssertionError) as e:
        ok(None, "should be truthy!")
    assert e.value.message == "should be truthy!"

def test_assert_equal_with_message_public():
    with pytest.raises(AssertionError) as e:
        equal('abc', 'def', "not the same")
    assert e.value.message == "not the same"

def test_assert_deep_equal_with_objects_public():
    deepEqual({'bar': 99}, {'bar': 99})
    with pytest.raises(AssertionError):
        deepEqual({'bar': 101}, {'bar': 202})

def test_assert_not_deep_equal_with_different_objects_public():
    notDeepEqual({'z': 10}, {'z': 20})
    with pytest.raises(AssertionError):
        notDeepEqual({'z': 88}, {'z': 88})