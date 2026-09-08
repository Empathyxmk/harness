"""
Public test for saxpy-usm3.cc with different input/output data (different vector size).
This test would invoke an executable; in the Python version we mimic its logic.
"""

import subprocess
import sys

def test_saxpy_usm3_uservalid_public(monkeypatch=None):
    exec_cmd = ["./saxpy-usm3.x", "14"]
    try:
        result = subprocess.run(exec_cmd, capture_output=True, text=True, check=False)
        out = result.stdout + result.stderr
    except FileNotFoundError:
        print("Public USM3 test skipped: saxpy-usm3.x not found (SYCL toolchain not present).")
        return
    if "Program completed without error." not in out:
        raise AssertionError(f"saxpy-usm3.x failed for vector length 14\nOutput:\n{out}")
    print("Public USM3 test ran successfully for vector length 14.")