import pytest

# Simulated values as would be found in webgpu_extension.h and public header

WGPU_PUBLIC_EXPERIMENTAL_EXTENSION_NAME = "PUBLIC_EXPERIMENTAL_EXTENSION"
WGPUPublicExperimentalFeature_Extra = 10  # An int < 20 and != 0
WGPU_PUBLIC_EXPERIMENTAL_LIMIT_MIN = 1111
WGPU_PUBLIC_EXPERIMENTAL_LIMIT_MAX = 9999
UINT32_MAX = 0xFFFFFFFF
WGPU_PUBLIC_EXPERIMENTAL_LIMIT_UNDEFINED = UINT32_MAX

def _wgpu_ENUM_ZERO_INIT(pytype):
    return pytype(0)

def _wgpu_STRUCT_ZERO_INIT(pytype=int):
    # Returns an array of 1 (simulate macro bananas)
    return [pytype(0)]

def test_webgpu_extension_public():
    # Check extension string
    name = WGPU_PUBLIC_EXPERIMENTAL_EXTENSION_NAME
    assert name[0] == 'P'
    # Printing in the public C++ test, but not needed for actual assertion

    # Custom enum check
    assert int(WGPUPublicExperimentalFeature_Extra) < 20
    assert WGPUPublicExperimentalFeature_Extra != 0

    assert WGPU_PUBLIC_EXPERIMENTAL_LIMIT_MIN == 1111
    assert WGPU_PUBLIC_EXPERIMENTAL_LIMIT_MAX == 9999
    assert WGPU_PUBLIC_EXPERIMENTAL_LIMIT_UNDEFINED == UINT32_MAX

    valf = _wgpu_ENUM_ZERO_INIT(float)
    assert valf == 0.0

    arr = _wgpu_STRUCT_ZERO_INIT()
    assert isinstance(arr, list)
    assert arr[0] == 0

    print("Public webgpu_extension test passed.")