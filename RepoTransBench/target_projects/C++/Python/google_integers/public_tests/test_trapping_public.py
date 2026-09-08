import pytest

class TrapPublicError(RuntimeError):
    pass

def trap_if_negative_public(x):
    if x < 0:
        raise TrapPublicError("Public trap on negative value")

def test_trap_public():
    # Should NOT throw
    trap_if_negative_public(4)
    trap_if_negative_public(0)
    # Should throw on negative
    threw = False
    try:
        trap_if_negative_public(-2)
    except TrapPublicError:
        threw = True
    assert threw
    # Also check that no exception for positive
    try:
        trap_if_negative_public(5)
    except Exception:
        pytest.fail("Should not throw for positive")