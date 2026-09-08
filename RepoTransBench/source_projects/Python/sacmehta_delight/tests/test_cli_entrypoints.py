import importlib
import sys
import types

import pytest

@pytest.mark.parametrize("filename,modname", [
    ("eval_lm", "fairseq_cli.eval_lm"),
    ("interactive", "fairseq_cli.interactive"),
    ("preprocess", "fairseq_cli.preprocess"),
])
def test_main_entrypoints(monkeypatch, filename, modname):
    called = {}
    monkeypatch.setitem(sys.modules, modname, types.SimpleNamespace(cli_main=lambda: called.setdefault("cli_main", True)))
    import runpy
    runpy.run_module(filename, run_name="__main__")
    assert called.get("cli_main")

def test_preprocess_main(monkeypatch):
    called = {}
    mod = types.SimpleNamespace(cli_main=lambda : called.setdefault("cli_main", True))
    sys.modules['fairseq_cli.preprocess'] = mod
    import preprocess
    if hasattr(preprocess, "__main__"):
        preprocess.__main__()
    else:
        preprocess.cli_main()
    assert called.get("cli_main")

def test_interactive_main(monkeypatch):
    called = {}
    mod = types.SimpleNamespace(cli_main=lambda : called.setdefault("cli_main", True))
    sys.modules['fairseq_cli.interactive'] = mod
    import interactive
    if hasattr(interactive, "__main__"):
        interactive.__main__()
    else:
        interactive.cli_main()
    assert called.get("cli_main")

def test_eval_lm_main(monkeypatch):
    called = {}
    mod = types.SimpleNamespace(cli_main=lambda : called.setdefault("cli_main", True))
    sys.modules['fairseq_cli.eval_lm'] = mod
    import eval_lm
    if hasattr(eval_lm, "__main__"):
        eval_lm.__main__()
    else:
        eval_lm.cli_main()
    assert called.get("cli_main")