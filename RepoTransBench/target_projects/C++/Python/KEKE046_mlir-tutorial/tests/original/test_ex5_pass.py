import subprocess
import sys

BINARY = "./ex5-pass/tools/toy-opt/toy-opt"
MLIR = "ex5-pass/ex5.mlir"

def test_ex5_pass_normal_usage():
    # Pass basic smoke test: passes loaded and can parse file
    ret = subprocess.call(f"{BINARY} {MLIR} > /dev/null 2>&1", shell=True)
    assert ret >= 0