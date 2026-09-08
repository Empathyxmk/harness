import sys
import importlib

def test_cnaturalneighbor_dummy_import(monkeypatch):
    modules_backup = sys.modules.copy()
    sys.modules.pop('cnaturalneighbor', None)
    import naturalneighbor.naturalneighbor as nn
    importlib.reload(nn)
    assert nn.cnaturalneighbor is None

def test_xyz_to_ijk_basic():
    import naturalneighbor.naturalneighbor as nn
    import numpy as np
    xyz = np.array([[1.0, 2.0, 3.0]])
    origin = [0.0, 0.0, 0.0]
    spacing = [1.0, 1.0, 1.0]
    ijk = nn._xyz_to_ijk(xyz, origin, spacing)
    np.testing.assert_array_equal(ijk, xyz)