import io
import sys
import pytest

"""
Translates the first version of the 'empty_braces_test_v1.cpp'.

C++ logic to Python:
- Class constructors and initializer_list cannot be exactly mimicked;
  we'll simulate the behavior by printing the same diagnostics.

All outputs are captured and tested.
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
        # Simulate both X() and X(initializer_list)
        # arg==None -> default, arg==list -> il ctor
        if arg is None:
            print("Def Ctor")
        else:
            print(f"il.size() = {len(arg)}")

def test_empty_braces_behavior_v1(capsys):
    # X<DefCtor> a0({});
    a0 = X([])
    # X<DefCtor> b0{{}};
    b0 = X([DefCtor()])
    # X<DeletedDefCtor> a2({});
    a2 = X([])
    # X<DeletedDefCtor> b2{{}};
    try:
        b2 = X([DeletedDefCtor()])
    except TypeError as e:
        print("error! attempt to use deleted constructor")
    # X<NoDefCtor> a1({});
    a1 = X([])
    # X<NoDefCtor> b1{{}};
    b1 = X([NoDefCtor(1)])

    captured = capsys.readouterr().out

    # Check printed output for key diagnostics:
    assert "il.size() = 0" in captured
    assert "il.size() = 1" in captured
    assert "error! attempt to use deleted constructor" in captured
    assert "Def Ctor" in captured