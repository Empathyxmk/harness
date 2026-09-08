import pytest
import json
from src.trurl_logic import run_trurl

with open("tests.json") as f:
    testdata = json.load(f)

@pytest.mark.parametrize("case", testdata)
def test_trurl_cases(case):
    arguments = case["input"]["arguments"]
    expected = case["expected"]
    stdout, stderr, returncode = run_trurl(arguments)
    if "stdout" in expected:
        assert stdout == expected["stdout"], f"stdout mismatch: expected {expected['stdout']!r}, got {stdout!r}"
    if "stderr" in expected:
        assert stderr == expected["stderr"], f"stderr mismatch: expected {expected['stderr']!r}, got {stderr!r}"
    if "returncode" in expected:
        assert returncode == expected["returncode"], f"returncode mismatch: expected {expected['returncode']}, got {returncode}"