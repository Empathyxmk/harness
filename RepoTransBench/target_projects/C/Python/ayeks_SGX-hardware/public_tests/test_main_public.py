import pytest
import sys
from io import StringIO
from contextlib import redirect_stdout

uint32_t = int

# --- Mock/Stub Functions (local to this public test file) ---
def native_cpuid32(leaf: uint32_t, eax, ebx, ecx, edx):
    if not all([eax, ebx, ecx, edx]):
        return -1
    eax[0] = 0x89ABCDEF
    ebx[0] = 0xFEDCBA98
    ecx[0] = 0xCAFEBABE
    edx[0] = 0xBAADF00D
    return 0

def cpuid_max_basic():
    return 0x18

def print_cpuid_enumeration():
    print("[MOCK] print_cpuid_enumeration (public)")

def native_rdmsr(msr: uint32_t, lo, hi):
    if lo: lo[0] = msr ^ 0xF0F0F0F0
    if hi: hi[0] = msr ^ 0x0F0F0F0F

def print_rdmsr_enumeration():
    print("[MOCK] print_rdmsr_enumeration (public)")

def print_vdso_enumeration():
    print("[MOCK] print_vdso_enumeration (public)")

def print_XSAVE_enumeration():
    print("[MOCK] print_XSAVE_enumeration (public)")

# --- Public Test Cases ---
def test_native_cpuid32_valid():
    eax = [0]
    ebx = [0]
    ecx = [0]
    edx = [0]
    native_cpuid32(0, eax, ebx, ecx, edx)
    assert eax[0] == 0x89ABCDEF, "cpuid32 eax different"
    assert ebx[0] == 0xFEDCBA98, "cpuid32 ebx different"
    assert ecx[0] == 0xCAFEBABE, "cpuid32 ecx different"
    assert edx[0] == 0xBAADF00D, "cpuid32 edx different"

def test_cpuid_max_basic():
    assert cpuid_max_basic() == 0x18, "cpuid_max_basic mismatch"

def test_native_rdmsr_valid():
    lo = [0]
    hi = [0]
    native_rdmsr(0x55, lo, hi)
    assert lo[0] == (0x55 ^ 0xF0F0F0F0), "rdmsr lo incorrect"
    assert hi[0] == (0x55 ^ 0x0F0F0F0F), "rdmsr hi incorrect"

def test_native_rdmsr_null():
    # Should not crash or write if None is passed (mimics C NULL)
    native_rdmsr(0xAA, None, None)

def test_print_functions(capsys):
    print_cpuid_enumeration()
    print_rdmsr_enumeration()
    print_vdso_enumeration()
    print_XSAVE_enumeration()
    captured = capsys.readouterr()
    assert "[MOCK] print_cpuid_enumeration (public)\n" in captured.out
    assert "[MOCK] print_rdmsr_enumeration (public)\n" in captured.out
    assert "[MOCK] print_vdso_enumeration (public)\n" in captured.out
    assert "[MOCK] print_XSAVE_enumeration (public)\n" in captured.out