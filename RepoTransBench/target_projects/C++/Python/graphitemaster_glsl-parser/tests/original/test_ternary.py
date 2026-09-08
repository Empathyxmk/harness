import pytest

def test_ternary_chain_assignments():
    a = 0.0
    b = 0.0
    c = 0.0
    d = 0.0

    w = ((a if a else b), c)
    z = (a if (b if c else d) else w)

    # Validate structure and precedence, not values
    assert w == (a if a else b, c)[1]
    assert isinstance(z, float)
    assert isinstance(w, float)