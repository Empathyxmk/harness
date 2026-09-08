import pytest
import sys

# Minimal simulation of debug.c

g_verbose = 0

def debug(fmt, *args):
    global g_verbose
    if not g_verbose:
        return
    print(fmt % args, file=sys.stderr, end='')

def test_debug_off(capsys):
    global g_verbose
    g_verbose = 0
    debug("This should not print: %d\n", 41)
    # Check that nothing printed to stderr
    captured = capsys.readouterr()
    assert captured.err == ""
    assert True  # Always passes (as in original)

def test_debug_on(capsys):
    global g_verbose
    g_verbose = 1
    debug("This should print: %d\n", 42)
    captured = capsys.readouterr()
    assert "This should print: 42" in captured.err
    assert True  # Always passes (as in original)