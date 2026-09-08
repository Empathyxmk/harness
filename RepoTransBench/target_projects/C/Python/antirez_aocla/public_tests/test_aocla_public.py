import pytest
from src.aocla.main import aocla_main

def test_no_input_file_case_public():
    """
    Public Test: run with argv0 (program name only), should print usage.
    Corresponds to test_aocla_basic_public.c
    Expected exit code 1 for missing input.
    """
    argv0 = ["alternative_progname"]
    rc = aocla_main(len(argv0), argv0)
    assert rc == 1, f"FAIL: [PUBLIC] Expected exit code 1 for missing input, got {rc}"
    print("PASS: [PUBLIC] no input file case")

def test_dummy_input_file_case_public():
    """
    Public Test: run with different dummy input file name, should "run" successfully.
    Corresponds to test_aocla_coverage_public.c
    Expected exit code 0 for input file present.
    """
    argv1 = ["alternative_progname", "public_test_script.aocla"]
    rc = aocla_main(len(argv1), argv1)
    assert rc == 0, f"FAIL: [PUBLIC] Expected exit code 0 for input file present, got {rc}"
    print("PASS: [PUBLIC] dummy input file case")