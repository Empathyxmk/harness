import pytest
import sys
from src import util

def test_dfu_debug_level_high(capfd, monkeypatch):
    """
    Corresponds to C's test_dfu_debug_level_high.
    Tests that a debug message with a level higher than the global debug level is NOT printed.
    """
    monkeypatch.setattr(util, '_debug_level', 100) # Set global debug level
    util.dfu_debug("testfile", "testfunc", 42, 150, "should not print: %d\n", 123)
    captured = capfd.readouterr() # Capture stdout and stderr
    assert captured.out == ""
    assert captured.err == ""

def test_dfu_debug_level_low(capfd, monkeypatch):
    """
    Corresponds to C's test_dfu_debug_level_low.
    Tests that a debug message with a level lower than or equal to the global debug level IS printed.
    """
    monkeypatch.setattr(util, '_debug_level', 100) # Set global debug level
    util.dfu_debug("testfile", "testfunc", 42, 50, "message: %s\n", "low-level debug")
    captured = capfd.readouterr() # Capture stdout and stderr
    assert "[testfile:testfunc:42] message: low-level debug\n" in captured.out
    assert captured.err == ""