import os
import tempfile
import shutil
import pytest

from src.getAllFiles import getAllFiles

def test_getAllFiles_nonexistent_directory():
    with pytest.raises(Exception):
        getAllFiles("nonexistent_folder")

def test_getAllFiles_empty_directory():
    folder = tempfile.mkdtemp()
    files = getAllFiles(folder)
    assert len(files) == 0
    shutil.rmtree(folder)