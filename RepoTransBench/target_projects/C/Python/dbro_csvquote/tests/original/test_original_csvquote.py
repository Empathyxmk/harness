import pytest
import os
import sys
from src.csvquote_wrapper.csvquote_cli import run_csvquote, read_file_content, write_file_content, compare_file_contents, assert_file_not_empty

# Path to test data files relative to this test file
ORIGINAL_TEST_DIR = os.path.dirname(__file__)
TESTDATA_CSV = os.path.join(ORIGINAL_TEST_DIR, "testdata.csv")
OUTPUT_TESTDATA_CSV = os.path.join(ORIGINAL_TEST_DIR, "output.testdata.csv")

@pytest.fixture(autouse=True)
def cleanup_temp_files():
    """Fixture to clean up temporary files after each test."""
    temp_files = [
        "output.testdata.csv.temp",
        "testdata.csv.temp",
        "test_customdelim.csv",
        "test_tabdelim.csv",
        "error_out.log"
    ]
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)
    yield
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)

def test_sanitize_succeeds():
    """1. Sanitize test (should succeed)"""
    output_temp_file = "output.testdata.csv.temp"
    stdout, stderr, retcode = run_csvquote([TESTDATA_CSV])
    write_file_content(output_temp_file, stdout)
    assert retcode == 0, f"Expected return code 0, got {retcode}. Stderr: {stderr}"
    assert compare_file_contents(OUTPUT_TESTDATA_CSV, output_temp_file), \
        f"Output file {output_temp_file} does not match {OUTPUT_TESTDATA_CSV}"

def test_round_trip_succeeds():
    """2. Round-trip test (should succeed)"""
    testdata_temp_file = "testdata.csv.temp"
    
    # First pass: csvquote testdata.csv
    stdout_first_pass, stderr_first_pass, retcode_first_pass = run_csvquote([TESTDATA_CSV])
    assert retcode_first_pass == 0, f"First pass failed. Stderr: {stderr_first_pass}"

    # Second pass: pipe output to csvquote -u
    stdout_second_pass, stderr_second_pass, retcode_second_pass = run_csvquote(["-u"], input_data=stdout_first_pass)
    write_file_content(testdata_temp_file, stdout_second_pass)

    assert retcode_second_pass == 0, f"Second pass failed. Stderr: {stderr_second_pass}"
    assert compare_file_contents(TESTDATA_CSV, testdata_temp_file), \
        f"Round-trip output {testdata_temp_file} does not match original {TESTDATA_CSV}"

def test_delimiter_quote_record_options():
    """3. Delimiter/quote/record options test"""
    output_file = "test_customdelim.csv"
    # Note: $'\t' in bash is a literal tab character. Python string '\t' achieves this.
    stdout, stderr, retcode = run_csvquote(["-d", "|", "-q", "'", "-r", "\t", TESTDATA_CSV])
    write_file_content(output_file, stdout)
    assert retcode == 0, f"Expected return code 0, got {retcode}. Stderr: {stderr}"
    assert assert_file_not_empty(output_file), f"Output file {output_file} is empty."

def test_tab_delimiter_option():
    """4. Tab delimiter via -t"""
    output_file = "test_tabdelim.csv"
    stdout, stderr, retcode = run_csvquote(["-t", TESTDATA_CSV])
    write_file_content(output_file, stdout)
    assert retcode == 0, f"Expected return code 0, got {retcode}. Stderr: {stderr}"
    assert assert_file_not_empty(output_file), f"Output file {output_file} is empty."

def test_edge_invalid_option():
    """5. Edge: invalid option"""
    error_log_file = "error_out.log"
    # The C script expects non-zero exit code on error and writes to stderr
    stdout, stderr, retcode = run_csvquote(["-z"])
    write_file_content(error_log_file, stderr) # Capture stderr to log file for analysis

    assert retcode != 0, f"Expected non-zero return code for invalid option, got {retcode}"
    # The original script uses `grep Unrecognized` which means it expects 'Unrecognized' in stderr
    assert "Unrecognized" in stderr, f"Expected 'Unrecognized' in stderr, got: {stderr}"
    assert os.path.exists(error_log_file), f"Error log file {error_log_file} was not created."
    assert "Unrecognized" in read_file_content(error_log_file), \
        f"Error log file {error_log_file} does not contain 'Unrecognized'."

@pytest.mark.parametrize("option,expected_error", [
    ("-d", "requires an operand"),
    ("-q", "requires an operand"),
    ("-r", "requires an operand"),
])
def test_edge_missing_operand(option, expected_error):
    """6-8. Edge: missing operand to -d, -q, -r"""
    error_log_file = "error_out.log"
    stdout, stderr, retcode = run_csvquote([option])
    write_file_content(error_log_file, stderr)

    assert retcode != 0, f"Expected non-zero return code for missing operand to {option}, got {retcode}"
    assert expected_error in stderr, f"Expected '{expected_error}' in stderr for {option}, got: {stderr}"
    assert os.path.exists(error_log_file), f"Error log file {error_log_file} was not created."
    assert expected_error in read_file_content(error_log_file), \
        f"Error log file {error_log_file} does not contain '{expected_error}' for {option}."