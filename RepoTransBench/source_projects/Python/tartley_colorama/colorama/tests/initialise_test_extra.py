# Extra coverage for initialise.py

import sys
import pytest
from colorama import initialise

def test_wipe_internal_state_for_tests_runs():
    initialise._wipe_internal_state_for_tests()
    # no error, nothing to assert

def test_init_and_deinit_wrap_false_conflicts():
    with pytest.raises(ValueError):
        initialise.init(autoreset=True, wrap=False)

def test_reinit_and_deinit(monkeypatch):
    # Setup globals to non-None to test code path
    monkeypatch.setattr(initialise, "wrapped_stdout", sys.stdout)
    monkeypatch.setattr(initialise, "wrapped_stderr", sys.stderr)
    monkeypatch.setattr(initialise, "orig_stdout", sys.stdout)
    monkeypatch.setattr(initialise, "orig_stderr", sys.stderr)
    initialise.reinit()
    initialise.deinit()

def test_just_fix_windows_console_shortcircuits(monkeypatch):
    monkeypatch.setattr(sys, "platform", "linux")
    assert initialise.just_fix_windows_console() is None

def test_colorama_text_context_manager():
    with initialise.colorama_text():
        assert True  # enter/exit