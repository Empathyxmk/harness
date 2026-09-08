import numpy as np
from normal_integration.core import (
    FFT_Poisson, DCT_Poisson, DST_Poisson, horn_brooks, tv_integration,
    phi1_integration, phi2_integration, smooth_integration,
)

def test_all_lambda_variants_public():
    p = np.array([[1,2],[0,1]])
    q = np.array([[0,1],[2,2]])
    mask = np.array([[1,1],[1,0]])
    lambda_ = np.ones((2,2)) * 0.03
    z0 = np.zeros((2,2))
    zinit = z0

    FFT_Poisson(p + q)
    DCT_Poisson(p, q)
    DST_Poisson(p, q, np.zeros((2,2)))
    horn_brooks(p, q, mask)
    tv_integration(p, q, mask, lambda_, z0, 0.1, 8, 1e-3, zinit)
    phi1_integration(p, q, mask, lambda_, z0, 0.1, 8, 1e-3, zinit)
    phi2_integration(p, q, mask, lambda_, z0, 0.1, 8, 1e-3, zinit)
    smooth_integration(p, q, mask, lambda_, z0, 'pcg', 'none')