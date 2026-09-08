import sys
import builtins
import importlib

def test_main_prints_custom_message(monkeypatch):
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
    # Purposefully require a different substring than in the original test
    assert "main application code" in captured[0]