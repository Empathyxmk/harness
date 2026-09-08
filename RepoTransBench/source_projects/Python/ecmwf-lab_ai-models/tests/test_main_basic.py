import pytest
import sys
import types

import src.ai_models.__main__ as mainmod

def test_main_help(monkeypatch, capsys):
    with pytest.raises(SystemExit):
        mainmod._main(['--help'])
    out = capsys.readouterr().out
    assert "usage:" in out or "Usage:" in out

def test_main_models(monkeypatch, capsys):
    # Patch available_models and sys.exit
    monkeypatch.setattr(mainmod, "available_models", lambda: ["foo", "bar"])
    def fake_exit(code):
        raise SystemExit()
    monkeypatch.setattr(sys, "exit", fake_exit)
    with pytest.raises(SystemExit):
        mainmod._main(['--models'])
    # List of models likely printed
    out = capsys.readouterr().out
    assert "foo" in out or "bar" in out

def test_main_verbose_debug(monkeypatch):
    # Patch argument parsing, just test argv parses and reaches end
    monkeypatch.setattr(mainmod, "available_models", lambda: ["foo"])
    monkeypatch.setattr(mainmod, "available_outputs", lambda: ["file"])
    monkeypatch.setattr(mainmod, "available_inputs", lambda: ["mars"])
    mainmod._main(['--verbose'])