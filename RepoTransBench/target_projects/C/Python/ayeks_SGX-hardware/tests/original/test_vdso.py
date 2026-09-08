import pytest
import sys
from io import StringIO
from contextlib import redirect_stdout

# --- Mock/Stub Functions (local to this test file) ---
def print_vdso_enumeration():
    print("[MOCK] print_vdso_enumeration (vdso)")

# --- Tests ---
def test_vdso_passes(capsys):
    print_vdso_enumeration()
    captured = capsys.readouterr()
    assert "[MOCK] print_vdso_enumeration (vdso)\n" in captured.out
    assert "vdso test PASSED\n" in captured.out # Original prints this itself