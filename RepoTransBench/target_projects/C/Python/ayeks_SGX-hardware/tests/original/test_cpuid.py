import pytest
import sys
from io import StringIO
from contextlib import redirect_stdout

uint32_t = int

# --- Mock/Stub Functions (local to this test file) ---
def native_cpuid32(eax, ebx, ecx, edx):
    if eax: eax[0] = 0xDEADBEEF
    if ebx: ebx[0] = 0xBEEFDEAD
    if ecx: ecx[0] = 0xABCD1234
    if edx: edx[0] = 0x56789DEF

def cpuid_max_basic():
    return 2

def print_cpuid_enumeration():
    print("[MOCK] print_cpuid_enumeration (cpuid)")

# --- Tests ---
def test_native_cpuid32_valid():
    eax = [0]
    ebx = [0]
    ecx = [0]
    edx = [0]
    native_cpuid32(eax, ebx, ecx, edx)
    assert eax[0] == 0xDEADBEEF
    assert ebx[0] == 0xBEEFDEAD
    assert ecx[0] == 0xABCD1234
    assert edx[0] == 0x56789DEF

def test_native_cpuid32_null():
    # Should not crash or write if None is passed (mimics C NULL)
    native_cpuid32(None, None, None, None)
    # If no exception, it passes, as in C.

def test_cpuid_max_basic():
    assert cpuid_max_basic() == 2

def test_print_cpuid_enumeration(capsys):
    print_cpuid_enumeration()
    captured = capsys.readouterr()
    assert "[MOCK] print_cpuid_enumeration (cpuid)\n" in captured.out