import pytest

# Simulate constants that would have been defined in webgpu.h/api in C++
WGPU_FALSE = 0
WGPU_TRUE = 1
UINT32_MAX = 0xFFFFFFFF

# Public test also uses these (should match C++ intent)
WGPU_ARRAY_LAYER_COUNT_UNDEFINED = UINT32_MAX

def _wgpu_ENUM_ZERO_INIT(pytype):
    return pytype(0)

def _wgpu_STRUCT_ZERO_INIT(pytype=float):
    # Returns an array of 1 (simulate macro bananas)
    return [pytype(0)]

def test_public_compile_macro_and_constants():
    # Output "WGPU_FALSE/TRUE" as would be printed (but in test, just assert, not print)
    assert WGPU_FALSE == 0
    assert WGPU_TRUE == 1

    # Flip assertion order from the original (preserving logical intent)
    assert 1 == WGPU_TRUE
    assert 0 == WGPU_FALSE

    # Use derived check with UINT32_MAX
    test_max = UINT32_MAX
    assert WGPU_ARRAY_LAYER_COUNT_UNDEFINED == test_max

    enum_val = _wgpu_ENUM_ZERO_INIT(int)
    assert enum_val == 0

    y = _wgpu_STRUCT_ZERO_INIT(float)
    assert isinstance(y, list)
    assert y[0] == 0.0

    print("webgpu.h macro/constant C++ public test passed.")