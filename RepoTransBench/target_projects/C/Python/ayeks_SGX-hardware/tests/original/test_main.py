import pytest
import sys
from io import StringIO
from contextlib import redirect_stdout

# Python equivalents of uint32_t for clarity, though standard int handles it.
# Using type hints for readability.
uint32_t = int

# --- Mock/Stub Functions (local to this test file, replicating C behavior) ---
def native_cpuid32(leaf: uint32_t, eax, ebx, ecx, edx):
    if not all([eax, ebx, ecx, edx]):
        return -1
    eax[0] = 0x12345678
    ebx[0] = 0x87654321
    ecx[0] = 0xDEADBEEF
    edx[0] = 0xBEEFDEAD
    return 0

def cpuid_max_basic():
    return 0x16

def print_cpuid_enumeration():
    print("[MOCK] print_cpuid_enumeration")

def native_rdmsr(msr: uint32_t, lo, hi):
    if not all([lo, hi]):
        return -1
    lo[0] = 0xAABBCCDD
    hi[0] = 0x11223344
    return 0

def print_rdmsr_enumeration():
    print("[MOCK] print_rdmsr_enumeration")

def print_vdso_enumeration():
    print("[MOCK] print_vdso_enumeration")

def print_XSAVE_enumeration():
    print("[MOCK] print_XSAVE_enumeration")

# --- Tests ---
def test_cpuid_basic():
    eax = [0] # Use lists to mimic C pointers for output parameters
    ebx = [0]
    ecx = [0]
    edx = [0]
    ret = native_cpuid32(0, eax, ebx, ecx, edx)
    assert ret == 0, "native_cpuid32 returned nonzero"
    assert eax[0] == 0x12345678, "EAX value wrong"
    assert ebx[0] == 0x87654321, "EBX value wrong"
    assert ecx[0] == 0xDEADBEEF, "ECX value wrong"
    assert edx[0] == 0xBEEFDEAD, "EDX value wrong"

def test_cpuid_max_basic():
    assert cpuid_max_basic() == 0x16, "cpuid_max_basic"

def test_cpuid_null_pointers():
    # In Python, passing None for pointers works similarly to C NULL
    assert native_cpuid32(0, None, None, None, None) == -1, "native_cpuid32 should fail on NULL"

def test_rdmsr_basic():
    lo = [0]
    hi = [0]
    ret = native_rdmsr(0, lo, hi)
    assert ret == 0, "native_rdmsr returned nonzero"
    assert lo[0] == 0xAABBCCDD, "rdmsr lo wrong"
    assert hi[0] == 0x11223344, "rdmsr hi wrong"

def test_rdmsr_null_pointers():
    assert native_rdmsr(0, None, None) == -1, "native_rdmsr should fail on NULL"

def test_print_functions(capsys):
    print_cpuid_enumeration()
    print_rdmsr_enumeration()
    print_vdso_enumeration()
    print_XSAVE_enumeration()
    captured = capsys.readouterr()
    assert "[MOCK] print_cpuid_enumeration\n" in captured.out
    assert "[MOCK] print_rdmsr_enumeration\n" in captured.out
    assert "[MOCK] print_vdso_enumeration\n" in captured.out
    assert "[MOCK] print_XSAVE_enumeration\n" in captured.out