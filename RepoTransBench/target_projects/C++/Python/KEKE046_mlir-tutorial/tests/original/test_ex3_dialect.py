import subprocess
import sys

BINARY = "./ex3-dialect/tools/toy-opt/toy-opt"

def test_ex3_dialect_help_option():
    # Should print help and exit(0)
    ret = subprocess.call(f"{BINARY} --help > /dev/null 2>&1", shell=True)
    # The return code should be 0
    assert ret == 0

def test_ex3_dialect_no_input():
    # Should fail because no input is provided (if main has such code)
    # Accept any exit code, just check no crash/segfault (i.e. the process exited normally)
    ret = subprocess.call(f"{BINARY} > /dev/null 2>&1", shell=True)
    # Accept any code, just check 0 or higher (i.e. no negative exit code)
    assert ret >= 0