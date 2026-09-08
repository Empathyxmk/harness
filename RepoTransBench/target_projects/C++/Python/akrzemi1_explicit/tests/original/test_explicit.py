import pytest
import types
from functools import wraps, partial

# --- Simulated xpl::is_signed_integral Type Trait ---

def is_signed_integral(py_type1, py_type2):
    """Simulate C++ type trait for checking if both types are the same and signed integral."""
    # In C++, is_signed_integral<T1,T2>::value is true if T1 and T2 are the same signed integer type
    # We'll implement for int, long, short, and exclude unsigned ints and floats/others.
    # In Python, no built-in unsigned int, so emulate types
    signed_types = {int}
    # For the spirit of C++ test, treat int as int, short, and long
    # Since all int in Python are signed
    is_same = py_type1 is py_type2
    return is_same and (py_type1 in signed_types)

# --- Simulated xpl::is_lvalue_ref_or_wrapper_ Type Trait ---

def is_lvalue_ref_or_wrapper_(base_type, other_type):
    """Simulate trait: is true if 'other_type' is an lvalue ref or reference wrapper for 'base_type'."""
    # In Python, all variables are references, but we'll simulate for the test.
    # We'll use the following convention:
    # - Just the same basic type: False (e.g., int, int)
    # - Python 'reference': if other_type is a function returning base_type (simulate lvalue ref)
    # - Simulate reference_wrapper as our own simple ReferenceWrapper class
    # - Accepts only 'ReferenceWrapper' or base_type

    # Simulate std::reference_wrapper with ReferenceWrapper
    class ReferenceWrapper:
        def __init__(self, value):
            self.value = value
    # Accept also parameterization with const (simulate with frozen dataclass)
    # Realistically, for the test, only type equivalence matters

    # Lvalue reference: in Python, not explicit.
    # For the test, emulate: other_type is a type that wraps base_type (ReferenceWrapper), or it's the type itself
    # We'll need to accept types. If other_type is a ReferenceWrapper of base_type, we treat as true.
    # But since we only check types (not values), use a marker
    # We'll match against an internal _ReferenceWrapper type

    # We'll need to pass marker types to the test function
    if getattr(other_type, '__name__', '') == 'ReferenceWrapper':
        # Simulate wrapper<base_type>
        return True
    if getattr(other_type, '__name__', '') == 'ConstReferenceWrapper':
        # Simulate wrapper<const base_type>
        return True
    if other_type is types.FunctionType:  # Simulate "int&"
        # Accept if the function returns base_type (simulate lvalue ref)
        return True
    return False

# -------------------------------------------------
# Utilities for the test cases to "simulate" C++ traits

class ReferenceWrapper:
    """Simulate std::reference_wrapper<T> holding a value of type T."""
    def __init__(self, value):
        self.value = value

class ConstReferenceWrapper:
    """Simulate std::reference_wrapper<const T> holding a value of type T."""
    def __init__(self, value):
        self.value = value

# ------------------- TESTS -----------------------

def test_is_signed_integral():
    # Use of only_when in simple trait cases...
    # int
    assert is_signed_integral(int, int) is True
    # For long, short: Python only has int (arbitrary precision signed int)
    # We'll treat int as covering all C++ signed ints: int, short, long
    assert is_signed_integral(int, int) is True
    assert is_signed_integral(int, int) is True
    # unsigned int: Python doesn't natively have it, so emulate with a custom type
    class UnsignedInt(int):
        pass
    assert is_signed_integral(UnsignedInt, UnsignedInt) is False
    # float
    assert is_signed_integral(float, float) is False
    # Plain char: implementation defined in C++, in Python is str of length 1, but do not check/assert
    # Just ensure it does not raise
    try:
        is_signed_integral(str, str)
    except Exception as exc:
        pytest.fail(f"Exception raised for str type in is_signed_integral: {exc}")

def test_is_lvalue_ref_or_wrapper():
    # Only lvalue reference ("int&") and reference_wrapper ("std::reference_wrapper<int>") should be true
    # Python can't model 'int&' directly, so we simulate with callable returning int (function type)

    # (int, int) -> False
    assert is_lvalue_ref_or_wrapper_(int, int) is False
    # (int, int&) ~ (int, function returning int): True
    def lvalue_ref(): return 0
    assert is_lvalue_ref_or_wrapper_(int, types.FunctionType) is True
    # (int, std::reference_wrapper<int>) -> True
    assert is_lvalue_ref_or_wrapper_(int, ReferenceWrapper) is True
    # (const int, std::reference_wrapper<const int>) -> True
    assert is_lvalue_ref_or_wrapper_(int, ConstReferenceWrapper) is True