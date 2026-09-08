import subprocess
import os
import sys
import re

BIN_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../bin/index.js"))

def test_basic_require_does_not_throw():
    # Just check if the file exists.
    assert os.path.exists(BIN_PATH)

def test_should_print_unknown_command_for_help_extra():
    # Use "node", not sys.executable (which is python), to execute JS.
    result = subprocess.run(
        ["node", BIN_PATH, "--help-extra"], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    assert re.search(r"Unknown command", result.stdout, re.I)

def test_should_print_output_for_version_extra():
    result = subprocess.run(
        ["node", BIN_PATH, "--version-extra"], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    assert len(result.stdout.strip()) > 0

def test_should_print_unknown_command_for_bogus_arg():
    result = subprocess.run(
        ["node", BIN_PATH, "--xyzPublic"], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    assert re.search(r"Unknown command", result.stdout, re.I)