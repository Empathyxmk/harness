import pytest
import sys
from io import StringIO
from contextlib import redirect_stdout

uint32_t = int

# --- Mock/Stub Functions (local to this public test file) ---
def native_rdmsr(msr: uint32_t, lo, hi):
    if lo: lo[0] = msr ^ 0xAAAAAAAA
    if hi: hi[0] = msr ^ 0x55555555

def print_rdmsr_enumeration():
    print("[MOCK] print_rdmsr_enumeration (rdmsr public)")

# --- Public Test Cases ---
def test_native_rdmsr_valid():
    lo = [0]
    hi = [0]
    native_rdmsr(0x99, lo, hi)
    assert lo[0] == (0x99 ^ 0xAAAAAAAA)
    assert hi[0] == (0x99 ^ 0x55555555)

def test_native_rdmsr_null():
    native_rdmsr(0xBB, None, None)

def test_print_rdmsr_enumeration(capsys):
    print_rdmsr_enumeration()
    captured = capsys.readouterr()
    assert "[MOCK] print_rdmsr_enumeration (rdmsr public)\n" in captured.out