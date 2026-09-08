import pytest
from unittest.mock import patch
import sys
import os
import io
from src.como_lang.mocks import read_line, ComoIO, como_stdin

# Helper to redirect stdin for test
@pytest.fixture
def set_stdin_public(request):
    original_stdin = sys.stdin
    temp_file_path = "test_input_public.txt"
    with open(temp_file_path, "w") as f:
        f.write(request.param)
    sys.stdin = open(temp_file_path, "r")
    yield
    sys.stdin.close()
    sys.stdin = original_stdin
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

@pytest.mark.parametrize("set_stdin_public", ["world\n"], indirect=True)
def test_read_line_normal_public(set_stdin_public):
    line = read_line()
    assert line == "world"

@pytest.mark.parametrize("set_stdin_public", ["   \n"], indirect=True)
def test_read_line_all_space_public(set_stdin_public):
    line = read_line()
    assert line == "   "

@pytest.mark.parametrize("set_stdin_public", ["foo\n"], indirect=True)
def test_read_line_eof_afterline_public(set_stdin_public):
    # Read first line
    line = read_line()
    assert line == "foo"

    # Now simulate EOF by replacing stdin with an empty stream
    with patch('sys.stdin', io.StringIO('')):
        line = read_line()
        assert line is None

def test_read_line_error_public():
    # Simulate an error by patching sys.stdin.readline to raise an exception
    with patch('sys.stdin.readline', side_effect=IOError("Simulated public read error")):
        line = read_line()
        assert line is None