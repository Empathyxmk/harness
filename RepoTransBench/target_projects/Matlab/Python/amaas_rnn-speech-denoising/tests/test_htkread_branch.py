import os
import pytest
import numpy as np
from src.htkread import htkread

def test_htkread_file_not_found():
    with pytest.raises(Exception):
        htkread('nonexistent_file.htk')

def test_htkread_unexpected_format(tmp_path):
    filename = tmp_path / "test_temp.htk"
    with filename.open("wb") as f:
        f.write(bytes([0, 0, 0, 1]))
    try:
        with pytest.raises(Exception):
            htkread(str(filename))
    finally:
        if filename.exists():
            filename.unlink()