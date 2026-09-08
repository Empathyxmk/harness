"""
User-space test for simple param error/edge handling logic, adapted from modttpoe/param.c
"""

import pytest

class KernelParam:
    def __init__(self, name):
        self.name = name

def ttp_param_dummy_set(val, kp):
    if kp is None:
        return -1
    print(f"{ttp_param_dummy_set.__name__}: Error: kernel param '{kp.name}' is not settable")
    return -2

def test_param_set():
    k1 = KernelParam("foo")
    r = ttp_param_dummy_set("bar", k1)
    assert r == -2

    # Test error on null pointer
    assert ttp_param_dummy_set("bar", None) == -1

def test_print_pass():
    # To reflect C main's print
    print("Param edge/error logic OK.")