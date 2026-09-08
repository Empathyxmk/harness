import pytest
from unittest.mock import patch
import sys
import os
from src.como_lang.mocks import read_line, ComoIO, como_stdin # Import como_stdin for patching

# Helper to redirect stdin for test
@pytest.fixture
def set_stdin(request):
    original_stdin = sys.stdin
    # Create a dummy file for stdin redirection, then clean it up
    temp_file_path = "test_input.txt"
    with open(temp_file_path, "w") as f:
        f.write(request.param)
    sys.stdin = open(temp_file_path, "r")
    yield
    sys.stdin.close()
    sys.stdin = original_stdin
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

@pytest.mark.parametrize("set_stdin", ["hello\n"], indirect=True)
def test_read_line_normal(set_stdin):
    line = read_line()
    assert line == "hello"

@pytest.mark.parametrize("set_stdin", ["\n"], indirect=True)
def test_read_line_empty(set_stdin):
    line = read_line()
    assert line == ""

def test_read_line_eof():
    # Simulate EOF by providing no input
    with patch('sys.stdin', io.StringIO('')):
        line = read_line()
        assert line is None

def test_read_line_error():
    # Simulate an error by mocking sys.stdin.readline to raise an exception
    with patch('sys.stdin.readline', side_effect=IOError("Simulated read error")):
        line = read_line()
        assert line is None