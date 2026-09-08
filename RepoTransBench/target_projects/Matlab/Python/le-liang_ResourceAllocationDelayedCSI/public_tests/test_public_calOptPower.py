import numpy as np
from tests.original.calOptPower_helper import calOptPower

def test_public_calOptPower():
    Pt = 8
    alpha = 2.6
    sigma2 = 0.1
    G = np.array([[2, 0.8], [0.9, 1.6]])
    y, _ = calOptPower([Pt, alpha], sigma2, 1, G, 0, 2)
    assert isinstance(y, (np.ndarray, list))
    if isinstance(y, np.ndarray):
        assert y.shape == (2,) or y.shape == (2,1)
        assert np.all(y >= 0)
    else:
        assert len(y) == 2 and all(elem >= 0 for elem in y)