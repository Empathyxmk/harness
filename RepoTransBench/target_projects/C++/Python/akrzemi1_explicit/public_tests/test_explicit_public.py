import pytest
import types

# --- Simulated public equivalents as above ---

def is_signed_integral(py_type1, py_type2):
    signed_types = {int}
    is_same = py_type1 is py_type2
    return is_same and (py_type1 in signed_types)

def is_lvalue_ref_or_wrapper_(base_type, other_type):
    # Simulate C++ 'is_lvalue_ref_or_wrapper_' to the extent possible in Python
    if getattr(other_type, '__name__', '') == 'ReferenceWrapper':
        return True
    if getattr(other_type, '__name__', '') == 'ConstReferenceWrapper':
        return True
    if other_type is types.FunctionType:
        return True
    return False

# Utilities for the test cases

class ReferenceWrapper:
    def __init__(self, value):
        self.value = value

class ConstReferenceWrapper:
    def __init__(self, value):
        self.value = value

def test_is_signed_integral_public():
    # Use "long long" (Python int), "unsigned long long" (simulate), "double" (Python float)
    # In Python, all ints are arbitrary-precision and signed.
    # So for "long long", just use int.
    assert is_signed_integral(int, int) is True
    # "unsigned long long": simulate with custom type
    class UnsignedLongLong(int): pass
    assert is_signed_integral(UnsignedLongLong, UnsignedLongLong) is False
    # double -> float in Python
    assert is_signed_integral(float, float) is False
    # 'signed char' is always signed in C++: simulate as int
    assert is_signed_integral(int, int) is True
    # 'unsigned char': simulate with custom unsigned type
    class UnsignedChar(int): pass
    assert is_signed_integral(UnsignedChar, UnsignedChar) is False
    # plain char: skip assertion, just ensure call doesn't error
    try:
        is_signed_integral(str, str)
    except Exception as exc:
        pytest.fail(f"Exception raised for str type in is_signed_integral: {exc}")

def test_is_lvalue_ref_or_wrapper_public():
    # Use 'double' and more reference_wrapper variations
    # double = float in Python
    # (double, double) --> (float, float): False
    assert is_lvalue_ref_or_wrapper_(float, float) is False
    # (double, double&) ~ (float, function returning float): True
    def lvalue_ref(): return 0.0
    assert is_lvalue_ref_or_wrapper_(float, types.FunctionType) is True
    # (double, std::reference_wrapper<double>)
    assert is_lvalue_ref_or_wrapper_(float, ReferenceWrapper) is True
    # (const double, std::reference_wrapper<const double>)
    assert is_lvalue_ref_or_wrapper_(float, ConstReferenceWrapper) is True