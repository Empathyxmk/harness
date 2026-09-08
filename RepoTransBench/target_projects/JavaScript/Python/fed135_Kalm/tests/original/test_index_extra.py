import importlib
import sys
import types

import pytest

def test_exports_components():
    import src
    # Test for required properties. In python, use hasattr or check keys.
    attrs = ['Client', 'Server', 'adapters', 'encoders', 'defaults', 'Adapter', 'Encoder']
    for attr in attrs:
        assert hasattr(src, attr)

def test_server_null_in_browser(monkeypatch):
    # Simulate platform 'browser' by patching platform.system()
    import src.index as module_under_test
    import src

    # We dynamically reload the module after patching
    import platform

    original_platform = platform.system

    monkeypatch.setattr(platform, "system", lambda: 'Browser')
    import importlib
    importlib.reload(src.index)
    assert getattr(src.index, "Server", None) is None
    monkeypatch.setattr(platform, "system", original_platform)
    # restore
    importlib.reload(src.index)