import importlib
import sys

def test_version_importable():
    # __version__ should always be importable and a string
    import honcho
    assert isinstance(honcho.__version__, str)
    assert len(honcho.__version__) > 0

def test_export_importable():
    import honcho
    assert hasattr(honcho, "export")
    # Should be a module
    assert getattr(honcho, "export").__name__ == "honcho.export"

def test_version_fallback(monkeypatch):
    # Simulate missing _version and fallback
    monkeypatch.setitem(sys.modules, "honcho._version", None)
    importlib.reload(sys.modules["honcho"])
    import honcho
    assert isinstance(honcho.__version__, str)