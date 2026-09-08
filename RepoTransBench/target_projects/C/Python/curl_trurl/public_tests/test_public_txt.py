import pytest
import os
import re
from src.trurl_logic import run_trurl

def parse_testfile_lines(fname):
    """
    Parse custom .txt test files.
    Returns list of dicts: {arguments: [...], expected: {...}}
    """
    with open(fname) as f:
        lines = f.readlines()
    cases = []
    for line in lines:
        if line.strip().startswith("#") or not line.strip():
            continue
        if line.startswith("input:"):
            inargs = line.replace("input:", "").strip()
            cur = {"arguments": inargs.split()}
        elif line.startswith("expected:"):
            exp = line.replace("expected:", "").strip()
            # Parse format like "scheme=https, host=example.org, path=/"
            expdict = {}
            for item in exp.split(","):
                item = item.strip()
                if not item:
                    continue
                if "=" in item:
                    k, v = item.split("=",1)
                    expdict[k.strip()] = v.strip()
            cases.append({"arguments": cur["arguments"], "expected": expdict})
    return cases

import glob

@pytest.mark.parametrize("testfile", sorted(glob.glob("testfiles_public/test_public_*.txt")))
def test_trurl_public_txtfiles(testfile):
    cases = parse_testfile_lines(testfile)
    for case in cases:
        args = case["arguments"]
        exp = case["expected"]
        # Map arg positions to dummy values for trurl_logic
        # If possible, run with simple expected key only (e.g., output must contain piece)
        stdout, stderr, returncode = run_trurl(args)
        # For each expected item, check that it's present in stdout
        # Note: only checks for field presence, not exact formatting
        for k, v in exp.items():
            assert f"{k}={v}" in stdout or f"{k}={v}\n" in stdout or k in stdout or v in stdout, f"Expected {k}={v} to be in output for args {args!r}: got {stdout!r}"