import numpy as np
import pytest
import naturalneighbor

def test_griddata_input_types():
    xyz = np.random.rand(5, 3).tolist()
    values = np.random.rand(5).tolist()
    xi = [[0, 1, 2], [2, 3, 4], [1, 2, 3]]
    with pytest.raises(ImportError):
        naturalneighbor.griddata(xyz, values, xi)

def test_griddata_nan_fillvalue(monkeypatch):
    import types
    import naturalneighbor.naturalneighbor as nn
    called = {}
    def dummy_griddata(xyz, values, xi, fill_value=np.nan):
        called['args'] = (xyz, values, xi, fill_value)
        return 123
    monkeypatch.setattr(nn, "cnaturalneighbor", types.SimpleNamespace(griddata=dummy_griddata))
    x = np.ones((2, 3))
    v = np.ones(2)
    xi = [[0, 1], [0, 1], [0, 1]]
    rv = nn.griddata(x, v, xi, fill_value=-42)
    assert called['args'][3] == -42
    assert rv == 123