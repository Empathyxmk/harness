import io
import sys
import pytest

"""
Translates the second version of the 'empty_braces_test_v2.cpp'.

C++ logic to Python:
- Like v1, but it does NOT expect the error (for b2), as in C++ that expr is commented out.
- The rest remains the same.
"""

class DefCtor:
    def __init__(self):
        pass

class DeletedDefCtor:
    def __init__(self):
        raise TypeError("DeletedDefCtor() is deleted in C++")

class NoDefCtor:
    def __init__(self, x):
        pass

class X:
    def __init__(self, arg=None):
        if arg is None:
            print("Def Ctor")
        else:
            print(f"il.size() = {len(arg)}")

def test_empty_braces_behavior_v2(capsys):
    a0 = X([])
    b0 = X([DefCtor()])
    a2 = X([])
    # X<DeletedDefCtor> b2{{}}; // error! attempt to use deleted constructor (commented out in v2)
    # Do not attempt to call X([DeletedDefCtor()]) here.
    a1 = X([])
    b1 = X([NoDefCtor(1)])

    captured = capsys.readouterr().out

    assert "il.size() = 0" in captured
    assert "il.size() = 1" in captured
    assert "Def Ctor" in captured