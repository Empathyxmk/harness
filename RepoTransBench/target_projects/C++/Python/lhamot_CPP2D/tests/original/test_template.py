import pytest

def sum_template(*args):
    if len(args) == 1:
        return args[0]
    else:
        return args[0] + sum_template(*args[1:])

def test_variadic_tmpl():
    assert sum_template(1, 0.5, 0.25) == 1.75

class S:
    val = 42

StatStruct = S()

def ret_ref():
    return StatStruct

def ret_ref_tmpl():
    return StatStruct

def test_return_ref_tmpl():
    a = ret_ref_tmpl()
    a.val = 43
    assert a.val == 43
    a.val = 44
    assert a.val == 44
    assert min(2, 3) == 2
    assert min(2, 3) == 2

def test_return_ref():
    a = ret_ref()
    a.val = 42
    assert a.val == 42
    a.val = 43
    assert a.val == 43

class QA:
    class B:
        pass

class QC_B:
    U = 18

def test_qualifier():
    assert QC_B.U == 18