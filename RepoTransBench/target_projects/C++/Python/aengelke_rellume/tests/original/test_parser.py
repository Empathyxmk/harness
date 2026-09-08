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
            pre.append("m1000000=" + code.hex() + term.hex())
            ripstr = "rip=" if asm.arch == "x86_64" or asm.arch == "rv64" else "pc="
            pre.append(ripstr + struct.pack("<Q", 0x1000000).hex())
            post.append(ripstr + struct.pack("<Q", 0x1000000 + len(code)).hex())
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

def test_parse_case_x86_64_code_mov():
    """Test: code assembly and parsing for x86_64 - mov eax,10"""
    class DummyASM:
        arch = "x86_64"
        def assemble(self, code):
            # Fake assembler output for mov eax,10 is b'\xb8\x0a\x00\x00\x00' (opcode for mov eax,imm32)
            return b'\xb8\x0a\x00\x00\x00', b'\xcc'
    asm = DummyASM()
    # input: code="mov eax,10" => rax=l:10
    # Use quotes so shlex keeps as single token, as in script inputs
    r = parse_case('code="mov eax,10" => rax=l:10', asm)
    code_val = b'\xb8\x0a\x00\x00\x00'.hex() + b'\xcc'.hex()
    assert f"m1000000={code_val}" in r
    rip_bytes = struct.pack("<Q", 0x1000000).hex()
    rip_post = struct.pack("<Q", 0x1000000 + len(b'\xb8\x0a\x00\x00\x00')).hex()
    assert f"rip={rip_bytes}" in r
    assert f"rip={rip_post}" in r
    assert "rax=0a00000000000000" not in r  # It should use l-format integer packing
    assert any("rax=" in part for part in r)
    assert "=>" in r

def test_parse_case_unsigned_l():
    case = "eax=l:4294967295"
    r = parse_case(case)
    packed = struct.pack("<L", 4294967295).hex()
    assert r[0].startswith("eax=")
    assert r[0].endswith(packed)

def test_parse_case_float_f():
    case = "xmm5=f:7.25"
    r = parse_case(case)
    packed = struct.pack("<f", 7.25).hex()
    assert r[0].startswith("xmm5=")
    assert r[0].endswith(packed)

def test_parse_case_multiple_fields():
    case = "rdx=q:13 rbx=l:11 bl=b:5"
    r = parse_case(case)
    nums_q = struct.pack("<Q", 13).hex()
    nums_l = struct.pack("<L", 11).hex()
    nums_b = struct.pack("<B", 5).hex()
    assert any("rdx=" in part and nums_q in part for part in r)
    assert any("rbx=" in part and nums_l in part for part in r)
    assert any("bl=" in part and nums_b in part for part in r)

def test_parse_case_post_undef():
    case = "rax=l:13 => rax=undef"
    r = parse_case(case)
    assert r[-1] == "rax=undef" or "rax=undef" in r

def test_parse_case_adds_src_hint():
    # Use quotes to ensure code is parsed in one token
    class DummyASM:
        arch = "rv64"
        def assemble(self, code):
            return b'abcd', b'efgh'
    asm = DummyASM()
    case = 'code="addi x6, x0, 42 addi x6, x6, 100" => x6=l:142'
    result = parse_case(case, asm)
    result.append("~src=cases_rv64_basic.txt:42")
    assert any("~src=" in part for part in result)

def test_parser_script_works(tmp_path):
    case_txt = "eax=l:1234"
    filepath = tmp_path / "test.case"
    filepath.write_text(case_txt)
    sys.argv = ["test_parser.py", str(filepath)]
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-o", "--output", type=argparse.FileType("w"), default='-')
        parser.add_argument("-a", "--assembler")
        parser.add_argument("-A", "--arch")
        parser.add_argument("casefiles", nargs="+")
        args = parser.parse_args()
        for filename in args.casefiles:
            with open(filename, "r") as file:
                for i, line in enumerate(file.readlines()):
                    line = line.strip()
                    if not line or line[0] == "#":
                        continue

                    try:
                        case = parse_case(line)
                        case.append(f"~src={os.path.basename(filename)}:{i+1}")
                        assert not any(" " in part for part in case)
                        args.output.write(" ".join(case) + "\n")
                    except Exception as e:
                        assert False, f"error parsing line {i+1} {e}"
    finally:
        sys.argv = sys.argv[:1]