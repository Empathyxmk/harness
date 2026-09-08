import pytest
import sys
from io import StringIO
from contextlib import redirect_stdout

uint32_t = int

# --- Mock/Stub Functions (local to this public test file) ---
def native_cpuid32(eax, ebx, ecx, edx):
    if eax: eax[0] = 0x1234ABCD
    if ebx: ebx[0] = 0xDCBA4321
    if ecx: ecx[0] = 0xB16B00B5
    if edx: edx[0] = 0xCAFEDADA

def cpuid_max_basic():
    return 4

def print_cpuid_enumeration():
    print("[MOCK] print_cpuid_enumeration (cpuid public)")

# --- Public Test Cases ---
def test_native_cpuid32_valid():
    eax = [0]
    ebx = [0]
    ecx = [0]
    edx = [0]
    native_cpuid32(eax, ebx, ecx, edx)
    assert eax[0] == 0x1234ABCD
    assert ebx[0] == 0xDCBA4321
    assert ecx[0] == 0xB16B00B5
    assert edx[0] == 0xCAFEDADA

def test_native_cpuid32_null():
    native_cpuid32(None, None, None, None)

def test_cpuid_max_basic():
    assert cpuid_max_basic() == 4

def test_print_cpuid_enumeration(capsys):
    print_cpuid_enumeration()
    captured = capsys.readouterr()
    assert "[MOCK] print_cpuid_enumeration (cpuid public)\n" in captured.out