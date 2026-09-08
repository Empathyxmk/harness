import argparse
import os
import shlex
import struct
import subprocess
import sys
import pytest

FMT_SUBST = {
    "b": ("B", lambda v: int(v, 0) % 0x100),
    "w": ("H", lambda v: int(v, 0) % 0x10000),
    "l": ("L", lambda v: int(v, 0) % 0x100000000),
    "q": ("Q", lambda v: int(v, 0) % 0x10000000000000000),
    "f": ("f", lambda v: float(v)),
    "d": ("d", lambda v: float(v)),
}

class Assembler:
    def __init__(self, proc, arch):
        self.proc = subprocess.Popen([proc, arch], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        self.arch = arch
    def assemble(self, code):
        self.proc.stdin.write("!ASM " + code + "\n")
        self.proc.stdin.flush()
        res = bytes.fromhex(self.proc.stdout.readline().strip())
        if self.arch == "x86_64":
            return res, b"\xcc" # term: int 3
        if self.arch == "rv64":
            return res, b"\x73\x00\x10\x00"
        if self.arch == "aarch64":
            return res, b"\x00\x00\x40\xd4" # term: hlt #0
    def close(self):
        self.proc.communicate()
        return self.proc.wait()

def parse_case(case, asm=None):
    pre, post = [], []
    cur = pre
    for i, part in enumerate(shlex.split(case)):
        if part == "!" and i == 0:
            pre.append("!")
            continue
        if part[:1] in "+-" and cur is pre:
            pre.append(part)
            continue
        if part == "=>":
            cur = post
            continue

        key, val = tuple(part.split("=", 2))
        if val == "undef":
            pass
        elif key == "code":
            if cur is not pre:
                raise Exception("code in post-check")
            code, term = asm.assemble(val)
            pre.append("m2000000=" + code.hex() + term.hex())
            ripstr = "rip=" if asm.arch == "x86_64" or asm.arch == "rv64" else "pc="
            pre.append(ripstr + struct.pack("<Q", 0x2000000).hex())
            post.append(ripstr + struct.pack("<Q", 0x2000000 + len(code)).hex())
            continue
        elif ":" in val:
            fmt, nums = tuple(val.split(":", 2))
            fmt, fns = zip(*(FMT_SUBST[c] for c in fmt))
            nums = [fn(v) for fn, v in zip(fns, nums.split(","))]
            val = struct.pack("<" + "".join(fmt), *nums).hex()
        else:
            val = bytes.fromhex(val).hex()
        cur.append("%s=%s"%(key, val))
    return pre + ["=>"] + post

# These public test cases match those found in the public version of the original script.
@pytest.mark.parametrize("arch, code, post_assert, field, expect", [
    ("x86_64", 'mov eax,10 inc eax',         'rax=l:11',  "rax", struct.pack("<L", 11).hex()),
    ("x86_64", 'mov rdx,5 add rdx,8',        'rdx=q:13',  "rdx", struct.pack("<Q", 13).hex()),
    ("x86_64", 'movaps xmm2,[rsp] paddd xmm2,xmm3', 'xmm2=q:1122334455667788,8877665544332211', "xmm2", struct.pack("<Q", 0x1122334455667788) + struct.pack("<Q", 0x8877665544332211)),
    ("rv64",   'addi x6, x0, 42 addi x6, x6, 100', 'x6=l:142',    "x6",  struct.pack("<L", 142).hex()),
    ("aarch64",'mov x7, #0xff00 add x7, x7, #255',   'x7=q:0x100ff', "x7", struct.pack("<Q", 0x100ff).hex()),
    ("x86_64", 'mov eax, -1',                     'eax=l:4294967295', "eax", struct.pack("<L", 4294967295).hex()),
    ("x86_64", 'movss xmm5,[rsp] addss xmm5,xmm6', 'xmm5=f:7.25',   "xmm5", struct.pack("<f", 7.25).hex()),
    ("rv64",   'ori x2, x0, 0xfff addi x2, x2, 1', 'x2=l:0x1000',  "x2", struct.pack("<L", 0x1000).hex()),
])
def test_public_parse_case_variants(arch, code, post_assert, field, expect):
    class DummyASM:
        def __init__(self):
            self.arch = arch
        def assemble(self, code_str):
            # Provide stable bytes for test validation.
            # Actual values don't matter for parse_case output, as long as m2000000 gets assembled + term bytes
            return b'\x66'*5, b'\xcc'
    asm = DummyASM()
    # Compose parse_case input like 'code=mov eax,10 inc eax => rax=l:11'
    icase = f"code={code} => {post_assert}"
    r = parse_case(icase, asm)
    m2000000_field = f"m2000000={(b'6666666666'+b'cc').hex()}"
    # Should have m2000000=..., rip=..., post field, etc.
    assert any(p.startswith("m2000000=") for p in r)
    assert any(p.startswith("rip=") or p.startswith("pc=") for p in r)
    # Should have "field=hex"
    assert "=>" in r
    has_field = [p for p in r if p.startswith(f"{field}=")]
    assert has_field, f"Missing field assignment for {field}"
    val = has_field[-1].split("=")[1]
    # Acceptable if lower-case, substring matching expected field
    assert expect.replace("0x", "").lower() in val.lower() or expect.lower() in val.lower()

def test_public_parse_case_unsigned_edge():
    # move -1 into eax
    class DummyASM:
        arch = "x86_64"
        def assemble(self, code):
            return b'\x99\x88', b'\xcc'
    asm = DummyASM()
    case = "code=mov eax, -1 => eax=l:4294967295"
    r = parse_case(case, asm)
    packed = struct.pack("<L", 4294967295).hex()
    has_field = [p for p in r if p.startswith("eax=")]
    assert has_field and has_field[-1].endswith(packed)

def test_public_parse_case_float():
    # movss xmm5,[rsp]; addss xmm5,xmm6 => xmm5=f:7.25
    class DummyASM:
        arch = "x86_64"
        def assemble(self, code):
            return b'\x55\x66', b'\xcc'
    asm = DummyASM()
    case = "code=movss xmm5,[rsp] addss xmm5,xmm6 => xmm5=f:7.25"
    r = parse_case(case, asm)
    packed = struct.pack("<f", 7.25).hex()
    has_field = [p for p in r if p.startswith("xmm5=")]
    assert has_field and packed in has_field[-1]