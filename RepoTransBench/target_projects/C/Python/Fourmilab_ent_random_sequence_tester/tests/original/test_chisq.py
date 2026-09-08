import pytest
from fourmilab_ent.chisq import pochisq

def test_pochisq():
    # These values are based on standard properties of chisq/normal distribution
    assert pochisq(0.0, 1) > 0.99
    v = pochisq(3.84, 1)
    assert 0.04 < v < 0.06  # about 5%, classic 1-df
    assert pochisq(10.0, 5) < 0.1
    # Test nonpositive input, which should result in a probability of 1.0 in our impl.
    assert pochisq(-1.0, 5) > 0.99 
    # Test df < 1, which should result in a probability of 1.0 in our impl.
    assert pochisq(5.0, 0) > 0.99