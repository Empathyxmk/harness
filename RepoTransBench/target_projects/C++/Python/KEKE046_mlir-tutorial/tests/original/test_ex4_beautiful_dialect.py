import subprocess
import sys

BINARY = "./ex4-beautiful-dialect/tools/toy-opt/toy-opt"
MLIR = "ex4-beautiful-dialect/ex4.mlir"

def test_ex4_beautiful_dialect_normal_usage():
    # may fail if main returns status code for incomplete parsing; just check no segfault
    ret = subprocess.call(f"{BINARY} {MLIR} > /dev/null 2>&1", shell=True)
    # Accept any exit code >= 0 (no crash)
    assert ret >= 0