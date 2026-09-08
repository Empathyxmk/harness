import os
import sys
import pytest

# Hypothetically imported function to be tested (examples/ls.c::_main)
# from src.examples.ls import _main

def _main(argc, argv):
    """
    Example stub. In real port, replace with 'ls' implementation.
    """
    if argc == 1:
        print('\n'.join(os.listdir(".")))
        return 0
    path = argv[1]
    if not os.path.isdir(path):
        return 1
    print('\n'.join(os.listdir(path)))
    return 0

def test_ls_no_args(capsys):
    argv = ["ls"]
    assert _main(1, argv) == 0
    out, _ = capsys.readouterr()
    assert out != ""

def test_ls_valid_dir(tmp_path, capsys):
    (tmp_path / "foo").mkdir()
    argv = ["ls", str(tmp_path)]
    assert _main(2, argv) == 0
    out, _ = capsys.readouterr()
    assert "foo" in out

def test_ls_invalid_dir():
    argv = ["ls", "doesnotexist"]
    assert _main(2, argv) != 0