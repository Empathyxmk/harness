import importlib
import sys

def test_init_runs():
    # Should not raise ImportError nor exception
    import pyicloud
    importlib.reload(pyicloud)
    assert hasattr(pyicloud, "__doc__")
    assert pyicloud.PyiCloudService is not None