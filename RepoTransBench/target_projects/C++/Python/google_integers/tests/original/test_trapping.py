import pytest

class TrapError(RuntimeError):
    pass

def trap_if_negative(x):
    if x < 0:
        raise TrapError("Trapped on negative value")

def test_trap_no_trap():
    trap_if_negative(1)
    trap_if_negative(0)

def test_trap_throws():
    threw = False
    try:
        trap_if_negative(-1)
    except TrapError:
        threw = True
    assert threw