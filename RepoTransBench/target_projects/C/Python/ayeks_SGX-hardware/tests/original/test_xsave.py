import pytest
import sys
from io import StringIO
from contextlib import redirect_stdout

# --- Mock/Stub Functions (local to this test file) ---
def print_XSAVE_enumeration():
    print("[MOCK] print_XSAVE_enumeration (xsave)")

# --- Tests ---
def test_xsave_passes(capsys):
    print_XSAVE_enumeration()
    captured = capsys.readouterr()
    assert "[MOCK] print_XSAVE_enumeration (xsave)\n" in captured.out
    assert "xsave test PASSED\n" in captured.out # Original prints this itself