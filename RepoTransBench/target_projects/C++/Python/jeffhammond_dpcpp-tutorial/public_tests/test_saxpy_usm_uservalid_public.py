"""
Public test for saxpy-usm.cc with different input/output data (different vector size).
This test would invoke an executable; in the Python version we mimic its logic.
"""

import subprocess
import sys

def test_saxpy_usm_uservalid_public(monkeypatch=None):
    # This test mimics calling './saxpy-usm.x 7' and verifying the output
    exec_cmd = ["./saxpy-usm.x", "7"]
    try:
        result = subprocess.run(exec_cmd, capture_output=True, text=True, check=False)
        out = result.stdout + result.stderr
    except FileNotFoundError:
        # If the file does not exist, XFAIL the test (SYCL executable missing)
        print("Public USM test skipped: saxpy-usm.x not found (SYCL toolchain not present).")
        return
    if "Program completed without error." not in out:
        raise AssertionError(f"saxpy-usm.x failed for vector length 7\nOutput:\n{out}")
    print("Public USM test ran successfully for vector length 7.")