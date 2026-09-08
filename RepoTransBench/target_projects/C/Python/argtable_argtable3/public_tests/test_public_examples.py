import pytest
import subprocess
import os

# Define the path to the compiled C example binaries
C_BIN_DIR = "examples_c_bin"

# Helper function to run C example programs and capture output/return code
def run_prog_capture(prog, args=None):
    program_path = os.path.join(C_BIN_DIR, prog)
    if not os.path.exists(program_path):
        pytest.fail(f"C example binary not found: {program_path}. Please ensure run_tests.sh was executed and compiled the examples.")

    cmd = [program_path]
    if args:
        cmd.extend(args.split()) # Simple split for space-separated args

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return result.stdout, result.stderr, result.returncode

# Test the examples/echo binary with different arguments than existing tests
def test_echo_public():
    # Single string, with -n
    stdout, stderr, rc = run_prog_capture("echo", "-n HelloWorld")
    assert rc == 0
    assert "option -n = YES" in stdout
    assert "HelloWorld" in stdout

    # Multiple strings, with -E (not -e)
    stdout, stderr, rc = run_prog_capture("echo", "-E This is public")
    assert rc == 0
    assert "option -E = YES" in stdout
    assert "This" in stdout and "public" in stdout

    # --version
    stdout, stderr, rc = run_prog_capture("echo", "--version")
    assert "echo v3" in stdout

    # --help
    stdout, stderr, rc = run_prog_capture("echo", "--help")
    assert "Usage: echo" in stdout
    assert "do not output the trailing newline" in stdout

    # Error: unknown option
    stdout, stderr, rc = run_prog_capture("echo", "--notarealopt")
    assert "Try 'echo --help' for more information." in stdout

# Test the examples/testargtable3 binary with different args
def test_testargtable3_public():
    # Simple file and -b
    stdout, stderr, rc = run_prog_capture("testargtable3", "-b input1.txt")
    assert rc == 0

    # Output file and scalar flag
    # Note: The C test for testargtable3 example itself doesn't print parsed values,
    # so we primarily check for successful execution (rc=0).
    stdout, stderr, rc = run_prog_capture("testargtable3", "-o outfile.txt --scalar=24 something.data")
    assert rc == 0

    # Help and version
    stdout, stderr, rc = run_prog_capture("testargtable3", "--help")
    assert "Usage: testargtable2.exe" in stdout # Matches original C output

    stdout, stderr, rc = run_prog_capture("testargtable3", "--version")
    assert "testargtable2.exe v3" in stdout # Matches original C output

    # Error: missing required file parameter
    stdout, stderr, rc = run_prog_capture("testargtable3", "-a")
    assert "Try 'testargtable2.exe --help' for more information." in stdout