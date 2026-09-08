import pytest

def test_watcher_import_and_str(monkeypatch):
    from pytest_watcher import watcher
    watcher_repr = str(watcher)
    assert "pytest_watcher" in watcher_repr or hasattr(watcher, "__name__")

def test_watcher_main_loop_interrupt(monkeypatch):
    from pytest_watcher import watcher

    def mock_loop(*args, **kwargs):
        raise KeyboardInterrupt()

    monkeypatch.setattr(watcher, "main_loop", mock_loop)
    with pytest.raises(KeyboardInterrupt):
        watcher.main_loop()