import sys
import os
import pytest

# Ensure src/ is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import protontricks.gui as gui

def test__run_gui_callederror(monkeypatch):
    # Patch `run` so that the first call raises CalledProcessError,
    # the retry raises gui.LocaleError, as is expected to test _run_gui handle.
    called = {"count": 0}

    class DummyLocaleError(gui.LocaleError):
        pass

    def fake_run(*a, **kw):
        if called["count"] == 0:
            called["count"] += 1
            raise gui.CalledProcessError(255, ['cmd'])
        else:
            # On retry, simulate unsupported locale and raise LocaleError
            raise gui.LocaleError("Locale error")

    monkeypatch.setattr(gui, "run", fake_run)

    with pytest.raises(gui.LocaleError):
        gui._run_gui(["foo"])