from qcore.testing import DummyObject, DummyMethodObject
from qcore.asserts import assert_eq, assert_is, assert_ne, AssertRaises

def test_public_dummy_object_attributes_are_set():
    x = DummyObject(a=2, b='foo')
    assert_eq(x.a, 2)
    assert_eq(x.b, 'foo')
    assert_is(x.c, None)

def test_public_dummy_object_comparison():
    x = DummyObject(a=2)
    y = DummyObject(a=2)
    z = DummyObject(a=3)
    assert_eq(x, y)
    assert_ne(x, z)

def test_public_dummy_method_object_call_and_args():
    d = DummyMethodObject()
    d(1, x=5)
    d(3, y='something')
    assert_eq(len(d.calls), 2)
    first_args, first_kwargs = d.calls[0]
    second_args, second_kwargs = d.calls[1]
    assert_eq(first_args, (1,))
    assert_eq(first_kwargs, {'x': 5})
    assert_eq(second_args, (3,))
    assert_eq(second_kwargs, {'y': 'something'})
    d.reset()
    assert_eq(d.calls, [])