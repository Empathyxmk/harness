import sys
import importlib

def test_cnaturalneighbor_dummy_import_public(monkeypatch):
    modules_backup = sys.modules.copy()
    sys.modules.pop("cnaturalneighbor", None)
    import naturalneighbor.naturalneighbor as nn
    importlib.reload(nn)
    assert nn.cnaturalneighbor is None

def test_xyz_to_ijk_basic_public():
    import naturalneighbor.naturalneighbor as nn
    import numpy as np
    xyz = np.array([[10.0, 20.0, 30.0]])
    origin = [5.0, 10.0, 15.0]
    spacing = [5.0, 10.0, 15.0]
    ijk = nn._xyz_to_ijk(xyz, origin, spacing)
    expected = np.array([[1.0, 1.0, 1.0]])
    np.testing.assert_array_equal(ijk, expected)