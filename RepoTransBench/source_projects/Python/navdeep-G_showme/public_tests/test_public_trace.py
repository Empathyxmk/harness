import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import showme

def test_trace_functionality(monkeypatch):
    from showme import core
    output = []
    def fake_print(*args, **kwargs):
        output.append(args)
    monkeypatch.setattr("builtins.print", fake_print)
    core.trace("Trace public test", 456)
    assert any("Trace public test" in str(arg) for tup in output for arg in tup)
    assert any("456" in str(arg) for tup in output for arg in tup)