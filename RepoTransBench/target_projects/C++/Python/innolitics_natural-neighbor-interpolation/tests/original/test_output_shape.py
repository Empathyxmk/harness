import numpy as np
import pytest
import naturalneighbor

def test_output_shape_importerror():
    xyz = np.array([[1,1,1], [2,2,2]])
    values = np.array([1, 2])
    xi = [[0, 1], [0, 1], [0, 1]]
    with pytest.raises(ImportError):
        naturalneighbor.griddata(xyz, values, xi)

def test_output_shape_dummy(monkeypatch):
    import types
    import naturalneighbor.naturalneighbor as nn
    dummy = types.SimpleNamespace(griddata=lambda *a, **k: np.ones((2,2,2)))
    monkeypatch.setattr(nn, "cnaturalneighbor", dummy)
    xyz = np.ones((2, 3))
    v = np.ones(2)
    xi = [[0, 1], [0, 1], [0, 1]]
    arr = nn.griddata(xyz, v, xi)
    assert arr.shape == (2, 2, 2)