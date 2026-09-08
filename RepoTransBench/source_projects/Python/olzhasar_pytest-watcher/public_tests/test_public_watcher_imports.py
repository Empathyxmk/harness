def test_public_import_all_watcher_module_names():
    import pytest_watcher.watcher as mod
    assert hasattr(mod, "__file__")
    assert callable(getattr(mod, "__loader__", lambda: True))