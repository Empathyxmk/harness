import numpy as np
from normal_integration.core import anisotropic_diffusion_integration

def test_aniso_diff_basic_public():
    p = np.ones((3,4)) * 3
    q = np.zeros((3,4))
    mask = np.ones((3,4))
    lambda_ = np.ones((3,4)) * 0.2
    z0 = np.zeros((3,4))
    z = anisotropic_diffusion_integration(p, q, mask, lambda_, z0, 0.1, 18, 1e-3, z0)
    assert z.shape == (3,4)

def test_aniso_diff_partial_mask_public():
    p = np.random.rand(4,2)
    q = np.random.rand(4,2)
    mask = np.array([[1,0],[1,1],[0,1],[1,1]])
    lambda_ = np.ones((4,2)) * 0.3
    z0 = np.zeros((4,2))
    z = anisotropic_diffusion_integration(p, q, mask, lambda_, z0, 0.15, 12, 1e-3, z0)
    assert z.shape == (4,2)