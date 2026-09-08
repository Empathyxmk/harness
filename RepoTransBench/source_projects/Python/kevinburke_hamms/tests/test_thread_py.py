import sys
import importlib

def test_thread_py_importable(monkeypatch):
    """Test importing thread.py without running main code (simulate __name__ != '__main__')."""
    module_name = "thread"
    if module_name in sys.modules:
        del sys.modules[module_name]
    # Patch sys.modules so __name__ is not "__main__"
    old_main = sys.modules.get("__main__")
    sys.modules["__main__"] = type("Dummy", (), {"__file__": "not_thread.py"})()
    try:
        importlib.import_module("thread")  # Should not raise
    finally:
        if old_main is not None:
            sys.modules["__main__"] = old_main
        else:
            del sys.modules["__main__"]

def test_thread_py_main(monkeypatch, capsys):
    import thread
    # Run the run_thread_example function, will use actual HammsServer
    thread.run_thread_example()
    captured = capsys.readouterr()
    assert "HammsServer started" in captured.out
    assert "stopping" in captured.out
    assert "HammsServer stopped" in captured.out