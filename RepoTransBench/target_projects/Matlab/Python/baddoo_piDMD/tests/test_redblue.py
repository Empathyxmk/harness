import numpy as np
from src.pidmd import redblue

def test_redblue():
    # Test custom colormap generation
    m = redblue(10)
    assert m.shape == (10, 3)
    assert m[0, 0] == 0 and m[-1, 0] == 1 and m[0, 2] == 1 and m[-1, 2] == 0