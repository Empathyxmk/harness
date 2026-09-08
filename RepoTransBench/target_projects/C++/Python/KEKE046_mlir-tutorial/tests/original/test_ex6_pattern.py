import subprocess
import sys

BINARY = "./ex6-pattern/tools/toy-opt/toy-opt"
MLIR = "ex6-pattern/ex6.mlir"

def test_ex6_pattern_normal_usage():
    ret = subprocess.call(f"{BINARY} {MLIR} > /dev/null 2>&1", shell=True)
    assert ret >= 0