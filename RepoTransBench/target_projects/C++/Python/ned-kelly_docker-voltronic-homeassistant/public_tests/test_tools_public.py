import io
import sys

import pytest
from src.inverter_cli import tools

def test_print_help_contains_supported_arguments(monkeypatch):
    captured = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', captured)
    res = tools.print_help()
    out = captured.getvalue()
    assert "SUPPORTED ARGUMENTS" in out
    assert res == 1