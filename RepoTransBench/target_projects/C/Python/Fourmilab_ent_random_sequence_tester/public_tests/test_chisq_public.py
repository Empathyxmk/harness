import pytest
from fourmilab_ent.chisq import pochisq

def test_pochisq_public():
    # Existing test: pochisq(0.0, 1), we use 0.5, 2 (should still be quite high)
    assert pochisq(0.5, 2) > 0.77
    # Existing: pochisq(3.84, 1) ~0.05, we use a 2-df classic value: 5.99 at df=2 ~0.05
    v = pochisq(5.99, 2)
    assert 0.04 < v < 0.06
    # Existing: pochisq(10.0, 5) < 0.1, let's use df=4 & chi=9.5 (~0.05)
    v_9_49 = pochisq(9.49, 4)
    assert 0.045 < v_9_49 < 0.055
    # Neg input; instead of -1.0, test -2.0
    assert pochisq(-2.0, 3) > 0.99
    # df < 1 edge; test (7.0, -2)
    assert pochisq(7.0, -2) > 0.99