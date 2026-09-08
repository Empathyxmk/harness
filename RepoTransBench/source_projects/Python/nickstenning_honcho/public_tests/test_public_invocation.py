import pytest
from honcho.__main__ import main

def test_main_invocation_public(monkeypatch):
    calls = []
    def fake_run():
        calls.append(True)
    monkeypatch.setattr("honcho.__main__.run", fake_run)
    monkeypatch.setattr("sys.argv", ["honcho", "start"])
    main()
    assert calls == [True]