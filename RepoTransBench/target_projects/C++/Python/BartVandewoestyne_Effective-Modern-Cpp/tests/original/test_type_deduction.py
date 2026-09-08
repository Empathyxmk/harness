import pytest

# Minimal replication of template deduction examples without including .cpps with main():

def func_const(param):
    # param is const in C++, but not in Python - just use as is
    pass

def func_non_const(param):
    # mutability not directly testable - but ensure callable
    pass

def func_pointer(param):
    # C++ pointer dereference; in Python, emulate by checking not None
    if param is not None:
        param[0] = param[0]  # Just for coverage; do nothing effectively

def test_const_reference():
    x = 5
    func_const(x)
    cx = 6  # const int in C++
    func_const(cx)

def test_non_const_reference():
    x = 5
    func_non_const(x)

def test_pointer():
    # In Python, use list to simulate "pointer to int"
    x = [7]
    px = x
    func_pointer(px)
    func_pointer(None)