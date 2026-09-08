import pytest

import typing

def is_nothrow_move_constructible(cls):
    # Python doesn't have nothrow guarantees; simulate always True for our 'Safe', else False
    return getattr(cls, "is_nothrow_move_constructible", False)


def is_assignable(lvalue_type, rvalue_type):
    # For our Safe/Val mockup
    return getattr(lvalue_type, "is_assignable", False)

def is_nothrow_move_assignable(cls):
    return getattr(cls, "is_nothrow_move_assignable", False)

class Val:
    is_nothrow_move_constructible = False
    is_assignable = False
    is_nothrow_move_assignable = False

class Safe:
    is_nothrow_move_constructible = True
    is_assignable = True
    is_nothrow_move_assignable = True

class Unsafe:
    is_nothrow_move_constructible = False
    is_assignable = True
    is_nothrow_move_assignable = False

class VoidNothrowBoth:
    is_nothrow_move_constructible = True
    is_nothrow_move_assignable = True

def test_type_traits_static_asserts():
    assert is_nothrow_move_constructible(Safe)
    assert not is_nothrow_move_constructible(Unsafe)
    assert is_assignable(Safe, Safe)
    assert not is_assignable(Val, Val)
    assert is_nothrow_move_assignable(Safe)
    assert not is_nothrow_move_assignable(Unsafe)
    assert is_nothrow_move_constructible(VoidNothrowBoth)
    assert is_nothrow_move_assignable(VoidNothrowBoth)