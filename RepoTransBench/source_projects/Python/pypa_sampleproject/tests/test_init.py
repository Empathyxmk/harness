import sys
import builtins
import importlib

def test_main_prints_message(monkeypatch):
    # Add src to sys.path if not present
    import os
    import pathlib

    project_root = pathlib.Path(__file__).parent.parent
    src_path = str(project_root / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    sample_init = importlib.import_module("sample.__init__")

    captured = []
    monkeypatch.setattr(builtins, "print", lambda msg: captured.append(msg))
    sample_init.main()
    assert "Call your main application code here" in captured[0]