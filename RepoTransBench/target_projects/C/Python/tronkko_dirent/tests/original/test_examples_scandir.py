import os
import sys
import glob
import tempfile
import pytest

# Hypothetically imported function to be tested (examples/scandir.c::_main)
# Replace with correct import in real port.
# from src.examples.scandir import _main

def _main(argc, argv):
    """
    Example stub. Replace with actual scandir logic.
    """
    if argc == 1:
        # List "."
        entries = os.listdir(".")
        for entry in entries:
            print(entry)
        return 0
    pattern = argv[1]
    matches = glob.glob(pattern)
    if not matches:
        print(f"no matches for {pattern}", file=sys.stderr)
        sys.exit(1)
    for match in matches:
        print(match)
    return 0

def test_scandir_list_current(capsys):
    argv = ["scandir"]
    _main(1, argv)
    out, _ = capsys.readouterr()
    assert "." in os.listdir(".") or out != ""

def test_scandir_glob(tmp_path, capsys):
    testdir = tmp_path / "1"
    testdir.mkdir()
    f = testdir / "file"
    f.write_text("data")
    argv = ["scandir", str(testdir / "*")]
    _main(2, argv)
    out, _ = capsys.readouterr()
    assert "file" in out

def test_scandir_specific_file(tmp_path, capsys):
    testdir = tmp_path / "1"
    testdir.mkdir()
    f = testdir / "file"
    f.write_text("data")
    argv = ["scandir", str(f)]
    _main(2, argv)
    out, _ = capsys.readouterr()
    assert "file" in out

def test_scandir_nonexistent(monkeypatch):
    argv = ["scandir", "ZZZ_NON_EXISTENT"]
    with pytest.raises(SystemExit) as e:
        _main(2, argv)
    assert e.value.code == 1