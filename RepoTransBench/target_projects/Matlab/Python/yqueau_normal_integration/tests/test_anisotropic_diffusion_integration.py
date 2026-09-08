import numpy as np
from normal_integration.core import anisotropic_diffusion_integration

def test_simple():
    p = np.ones((4, 4))
    q = np.ones((4, 4))
    mask = np.ones((4, 4))
    z = anisotropic_diffusion_integration(p, q, mask)
    assert z.shape == (4, 4)
    assert np.all(np.isfinite(z))

def test_with_default_mask():
    p = np.random.rand(5, 5)
    q = np.random.rand(5, 5)
    z = anisotropic_diffusion_integration(p, q)
    assert z.shape == (5, 5)
    assert np.all(np.isfinite(z))