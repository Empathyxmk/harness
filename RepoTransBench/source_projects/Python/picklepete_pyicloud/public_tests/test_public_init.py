import importlib
import sys

def test_init_runs_public():
    # Should not raise ImportError nor exception
    import pyicloud
    importlib.reload(pyicloud)
    assert hasattr(pyicloud, "__doc__")
    assert hasattr(pyicloud, "PyiCloudService")
    assert pyicloud.PyiCloudService.__name__ == "PyiCloudService"