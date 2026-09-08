import pytest
from src.jxck_assert import *

def test_assert_ok_truthy():
    ok(True)
    ok(1)

def test_assert_ok_falsy_throws():
    with pytest.raises(Exception):
        ok(False)
    with pytest.raises(Exception):
        ok(0)

def test_assert_equal():
    equal(1, 1)
    equal(1, '1')
    with pytest.raises(Exception):
        equal(1, 2)

def test_assert_not_equal():
    notEqual(1, 2)
    with pytest.raises(Exception):
        notEqual(1, 1)

def test_assert_deep_equal():
    deepEqual({'a': {'b': 1}}, {'a': {'b': 1}})
    with pytest.raises(Exception):
        deepEqual({'a': 1}, {'a': 2})

def test_assert_not_deep_equal():
    notDeepEqual({'a': 1}, {'a': 2})
    with pytest.raises(Exception):
        notDeepEqual({'a': 1}, {'a': 1})

def test_assert_strict_equal_and_not_strict_equal():
    strictEqual(1, 1)
    with pytest.raises(Exception):
        strictEqual(1, "1")
    notStrictEqual(1, 2)
    with pytest.raises(Exception):
        notStrictEqual(1, 1)

def test_assert_throws():
    throws(lambda: (_ for _ in ()).throw(Exception("test")))
    with pytest.raises(Exception):
        throws(lambda: None)

def test_assert_does_not_throw():
    doesNotThrow(lambda: None)
    with pytest.raises(Exception):
        doesNotThrow(lambda: (_ for _ in ()).throw(Exception()))

def test_if_error():
    ifError(None)
    ifError(None)
    ifError(0)
    ifError('')
    with pytest.raises(Exception):
        ifError(Exception("boom"))


def test_assert_ok_with_custom_message():
    with pytest.raises(AssertionError) as e:
        ok(False, "fail message")
    assert e.value.message == "fail message"

def test_assert_equal_with_message():
    with pytest.raises(AssertionError) as e:
        equal(1, 2, "not equal")
    assert e.value.message == "not equal"

def test_assert_deep_equal_with_objects():
    deepEqual({'foo': 1}, {'foo': 1})
    with pytest.raises(Exception):
        deepEqual({'foo': 1}, {'foo': 2})

def test_assert_not_deep_equal_with_different_objects():
    notDeepEqual({'foo': 1}, {'foo': 2})
    with pytest.raises(Exception):
        notDeepEqual({'foo': 1}, {'foo': 1})