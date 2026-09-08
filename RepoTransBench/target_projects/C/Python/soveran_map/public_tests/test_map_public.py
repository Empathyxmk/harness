import pytest
import os

# Path to the public test input file
PUBLIC_INPUT_FILE_PATH = "test_inputs/public_input"

def test_normal_usage_one_line_input_command_using_variable_public(run_map_command_fixture):
    """
    Test: normal usage with one-line input, command using the variable (public input).
    Corresponds to: assert_equal "barbar" "$(printf bar | ./map v 'printf $v$v')"
    """
    input_data = "bar"
    expected_output = "barbar"
    stdout, _, _ = run_map_command_fixture(["v", "printf $v$v"], input_data=input_data)
    assert stdout == expected_output

def test_multi_line_input_using_public_input_file(run_map_command_fixture):
    """
    Test: multi-line input using public input file.
    Corresponds to: assert_equal "helloworldtest" "$(cat ./test/public_input | ./map v 'printf $v')"
    """
    with open(PUBLIC_INPUT_FILE_PATH, 'r') as f:
        input_data = f.read()
    expected_output = "helloworldtest"
    stdout, _, _ = run_map_command_fixture(["v", "printf $v"], input_data=input_data)
    assert stdout == expected_output

def test_edge_case_empty_stdin_public(run_map_command_fixture):
    """
    Test: edge case: empty stdin (no input, should not call command).
    Corresponds to: output=$(echo -n "" | ./map XX 'echo none'); assert_equal "" "$output"
    """
    expected_output = ""
    stdout, _, _ = run_map_command_fixture(["XX", "echo none"], input_data="")
    assert stdout == expected_output

def test_single_character_input_public(run_map_command_fixture):
    """
    Test: single character input (public char).
    Corresponds to: assert_equal "zz" "$(echo "z" | ./map v 'printf $v$v')"
    """
    input_data = "z"
    expected_output = "zz"
    stdout, _, _ = run_map_command_fixture(["v", "printf $v$v"], input_data=input_data)
    assert stdout == expected_output

def test_input_with_only_newline_public(run_map_command_fixture):
    """
    Test: input with only a newline ('\\n'; llen == 1, should not run command).
    Corresponds to: output=$(printf "\n" | ./map v 'echo fail'); assert_equal "" "$output"
    """
    input_data = "\n"
    expected_output = ""
    stdout, _, _ = run_map_command_fixture(["v", "echo fail"], input_data=input_data)
    assert stdout == expected_output

def test_usage_error_argc_not_3_public(run_map_command_fixture):
    """
    Test: usage error, argc != 3 (should exit with message and code 1).
    Corresponds to: ./map > public_output.txt 2>&1; code=$?; grep -q "usage: " public_output.txt && [ "$code" = "1" ]
    """
    stdout, stderr, returncode = run_map_command_fixture([], check_returncode=False)
    # Check if "usage:" string is present in either stdout or stderr and exit code is 1
    assert ("usage:" in stderr or "usage:" in stdout), "Expected 'usage:' message in output"
    assert returncode == 1, "Expected exit code 1 for usage error"