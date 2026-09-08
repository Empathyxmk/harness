import io
import os
import sys

import pytest

from src.inverter_cli import tools

def test_print_help_returns_1(monkeypatch):
    captured = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', captured)
    res = tools.print_help()
    out = captured.getvalue()
    assert "USAGE" in out
    assert res == 1

def test_lprintf_with_debug_flag(tmp_path, monkeypatch):
    # Patch global debugFlag and LOG_FILE
    monkeypatch.setattr(tools, "debugFlag", True)
    monkeypatch.setattr(tools, "LOG_FILE", str(tmp_path / "debug.log"))
    # Remove log file if exists (it won't at tmp_path)
    log_file = tmp_path / "debug.log"
    if log_file.exists():
        log_file.unlink()
    captured = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', captured)
    tools.lprintf("This is a %s: %d", "test", 123)
    out = captured.getvalue()
    assert "This is a test: 123" in out
    # Check log file contents
    with open(log_file, "r") as f:
        data = f.read()
        assert "This is a test: 123" in data
    # Reset debugFlag
    monkeypatch.setattr(tools, "debugFlag", False)

def test_lprintf_without_debug_flag(monkeypatch):
    monkeypatch.setattr(tools, "debugFlag", False)
    captured = io.StringIO()
    sys.stdout = captured
    try:
        tools.lprintf("Should not print %d", 99)
    finally:
        sys.stdout = sys.__stdout__
    assert captured.getvalue() == ""