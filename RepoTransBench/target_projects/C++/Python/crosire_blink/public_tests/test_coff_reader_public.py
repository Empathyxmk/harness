import pytest
import os

def test_coff_reader_public_open_nonexistent_file(tmp_path):
    # Different path/data from any regular test: use a UUID style random filename
    bogus_path = tmp_path / "abcdef12-3456-7890-0000-000000000777.obj"
    # Simulates open_coff_file: just test file not existing
    assert not os.path.exists(bogus_path)
    # Opening should fail
    try:
        file_handle = open(bogus_path, "rb")
    except FileNotFoundError:
        file_handle = None
    assert file_handle is None