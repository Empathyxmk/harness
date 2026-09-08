import pytest
from src.aocla.main import aocla_main

def test_no_input_file_case_original():
    """
    Original Test: Basic smoke test: run with no args, should print usage.
    Corresponds to test_aocla_basic.c
    Expected exit code 1 for no input.
    """
    argv0 = ["progname"]
    rc = aocla_main(len(argv0), argv0)
    assert rc == 1, f"FAIL: Expected exit code 1 for no input, got {rc}"
    print("PASS: no input file case")

def test_dummy_input_file_case_original():
    """
    Original Test: run with dummy input file name, should "run" successfully.
    Corresponds to test_aocla_coverage.c
    Expected exit code 0 for input file present.
    """
    argv1 = ["progname", "dummy.aocla"]
    rc = aocla_main(len(argv1), argv1)
    assert rc == 0, f"FAIL: Expected exit code 0 for input file present, got {rc}"
    print("PASS: dummy input file case")