import pytest
import numpy as np

import naturalneighbor

def test_griddata_importerror(monkeypatch):
    import naturalneighbor.naturalneighbor as nn
    monkeypatch.setattr(nn, "cnaturalneighbor", None)
    x = np.random.rand(5, 3)
    v = np.random.rand(5)
    xi = [0, 1, 2]
    with pytest.raises(ImportError):
        naturalneighbor.griddata(x, v, xi)

def test_griddata_dummy(monkeypatch):
    import types
    import naturalneighbor.naturalneighbor as nn
    dummy = types.SimpleNamespace(griddata=lambda *a, **k: 'dummy result')
    monkeypatch.setattr(nn, "cnaturalneighbor", dummy)
    x = np.ones((1, 3))
    v = np.ones(1)
    xi = [0]
    result = nn.griddata(x, v, xi)
    assert result == 'dummy result'

def test_xyz_to_ijk_vectorized():
    import naturalneighbor.naturalneighbor as nn
    import numpy as np
    xyz = np.array([[5, 6, 7], [2, 4, 8]])
    origin = np.array([1, 2, 3])
    spacing = np.array([2, 2, 2])
    expected = (xyz - origin) / spacing
    np.testing.assert_array_equal(nn._xyz_to_ijk(xyz, origin, spacing), expected)

def test_xyz_to_ijk_scalar():
    import naturalneighbor.naturalneighbor as nn
    import numpy as np
    xyz = np.array([2, 4, 6])
    origin = np.array([0, 0, 0])
    spacing = np.array([2, 2, 2])
    expected = xyz / spacing
    np.testing.assert_allclose(nn._xyz_to_ijk(xyz, origin, spacing), expected)