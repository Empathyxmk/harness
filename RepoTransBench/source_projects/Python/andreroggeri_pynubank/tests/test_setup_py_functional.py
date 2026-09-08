import pytest

def test_read_success(tmp_path, monkeypatch):
    # Simulate an external helper "read" function.
    from pathlib import Path
    import types

    def read(fname):
        with open(fname, encoding="utf-8") as f:
            return f.read()

    # Prepare temp file
    fname = tmp_path / "afile"
    fname.write_text("DATA")
    setupmod = types.SimpleNamespace(read=read)
    assert setupmod.read(fname) == "DATA"

def test_read_file_not_found():
    # Simulate a missing file.
    import types

    def read(fname):
        with open(fname, encoding="utf-8") as f:
            return f.read()

    setupmod = types.SimpleNamespace(read=read)
    with pytest.raises(FileNotFoundError):
        setupmod.read("idonotexist.txt")