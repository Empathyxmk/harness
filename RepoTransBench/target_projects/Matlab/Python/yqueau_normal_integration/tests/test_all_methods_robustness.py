import numpy as np
from normal_integration.core import (
    tv_integration,
    smooth_integration,
    phi1_integration,
    phi2_integration,
    anisotropic_diffusion_integration,
    mumford_shah_integration,
    horn_brooks,
)

def test_all_zero_input():
    sz = (3, 3)
    input_p = np.zeros(sz)
    input_q = np.zeros(sz)

    func_list = [
        tv_integration,
        smooth_integration,
        phi1_integration,
        phi2_integration,
        anisotropic_diffusion_integration,
        mumford_shah_integration,
        horn_brooks,
    ]
    for func in func_list:
        z = func(input_p, input_q)
        assert z.shape == sz
        assert np.all(np.isfinite(z))

def test_mask_edge_case():
    p = np.random.rand(3, 3)
    q = np.random.rand(3, 3)
    mask = np.zeros((3, 3))
    func_list = [
        tv_integration,
        smooth_integration,
        phi1_integration,
        phi2_integration,
        anisotropic_diffusion_integration,
        mumford_shah_integration,
        horn_brooks,
    ]
    for func in func_list:
        z = func(p, q, mask)
        assert z.shape == p.shape