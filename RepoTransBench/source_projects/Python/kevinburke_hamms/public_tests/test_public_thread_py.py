import sys
import importlib

def test_thread_py_importable_custom(monkeypatch):
    """Public Test: Importing thread.py with a different dummy main name."""
    module_name = "thread"
    if module_name in sys.modules:
        del sys.modules[module_name]
    # Patch sys.modules so __name__ is not "__main__"
    old_main = sys.modules.get("__main__")
    sys.modules["__main__"] = type("DummyMain", (), {"__file__": "custom_dummy.py"})()
    try:
        importlib.import_module("thread")  # Should not raise
    finally:
        if old_main is not None:
            sys.modules["__main__"] = old_main
        else:
            del sys.modules["__main__"]

def test_thread_py_main_custom(monkeypatch, capsys):
    import thread
    # The test uses the main logic but will check a different output substring
    thread.run_thread_example()
    captured = capsys.readouterr()
    # Instead of "HammsServer stopped", check for "started" in the beginning and "stop" in the end
    lines = captured.out.strip().splitlines()
    assert any("HammsServer started" in l for l in lines)
    assert lines[-2].strip().lower() == "stopping"  # check the stopping print
    assert "HammsServer stopped" in lines[-1]