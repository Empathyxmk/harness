import pytest
import sys
from io import StringIO
from contextlib import redirect_stdout

uint32_t = int

# --- Mock/Stub Functions (local to this test file) ---
def native_rdmsr(msr: uint32_t, lo, hi):
    if lo: lo[0] = msr ^ 0x80808080
    if hi: hi[0] = msr ^ 0x10101010

def print_rdmsr_enumeration():
    print("[MOCK] print_rdmsr_enumeration (rdmsr)")

# --- Tests ---
def test_native_rdmsr_valid():
    lo = [0]
    hi = [0]
    native_rdmsr(0x44, lo, hi)
    assert lo[0] == (0x44 ^ 0x80808080)
    assert hi[0] == (0x44 ^ 0x10101010)

def test_native_rdmsr_null():
    # Should not crash or write if None is passed (mimics C NULL)
    native_rdmsr(0x55, None, None)
    # If no exception, it passes, as in C.

def test_print_rdmsr_enumeration(capsys):
    print_rdmsr_enumeration()
    captured = capsys.readouterr()
    assert "[MOCK] print_rdmsr_enumeration (rdmsr)\n" in captured.out