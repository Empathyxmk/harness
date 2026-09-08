import importlib
import sys
import types
import pytest

def test_exports_all_main_components_public():
    import src
    for prop in ['Encoder', 'Adapter', 'defaults', 'encoders', 'adapters', 'Server', 'Client']:
        assert hasattr(src, prop)

def test_server_null_with_explicit_browser_string_public(monkeypatch):
    import src.index as module_under_test
    import src
    import platform

    original_platform = platform.system

    monkeypatch.setattr(platform, "system", lambda: 'Browser')
    import importlib
    importlib.reload(src.index)
    assert getattr(src.index, "Server", None) is None
    monkeypatch.setattr(platform, "system", original_platform)
    # restore
    importlib.reload(src.index)