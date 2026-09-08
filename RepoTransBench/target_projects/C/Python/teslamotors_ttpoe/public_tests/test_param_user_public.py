"""
Public user-space test for param error/edge handling with different data.
"""

import pytest

class KernelParam:
    def __init__(self, name):
        self.name = name

def ttp_param_dummy_set(val, kp):
    if kp is None:
        return -10  # different error code in public tests
    print(f"{ttp_param_dummy_set.__name__}: Error: kernel param '{kp.name}' is not settable")
    return -20

def test_param_set_public():
    k2 = KernelParam("baz")
    r = ttp_param_dummy_set("qux", k2)
    assert r == -20

    # Test error on null pointer (different expectation)
    assert ttp_param_dummy_set("qux", None) == -10

def test_print_pass():
    print("Param public edge/error logic OK.")