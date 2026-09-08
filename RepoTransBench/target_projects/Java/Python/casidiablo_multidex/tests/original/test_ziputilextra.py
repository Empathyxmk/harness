import pytest
import tempfile
import zipfile
import os

class ZipUtil:
    @staticmethod
    def find_central_directory(raf):
        raf.seek(0, os.SEEK_END)
        file_size = raf.tell()
        if file_size < 22:
            raise zipfile.BadZipFile("File too short for central directory")

def test_find_central_directory_short_file(tmp_path):
    path = tmp_path / "shortzip.zip"
    with open(path, "wb") as f:
        f.write(b"\x00")
    with open(path, "rb") as raf:
        with pytest.raises(zipfile.BadZipFile):
            ZipUtil.find_central_directory(raf)

def test_find_central_directory_short_file_cover(tmp_path):
    # This test covers calling with a length exactly zero and exactly 21
    path = tmp_path / "shortzip2.zip"
    with open(path, "wb") as f:
        f.write(b"")  # length 0, invalid for zip
    with open(path, "rb") as raf:
        with pytest.raises(zipfile.BadZipFile):
            ZipUtil.find_central_directory(raf)
    # Now 21 bytes (still invalid: must be >=22 for central directory)
    path2 = tmp_path / "shortzip3.zip"
    with open(path2, "wb") as f:
        f.write(b"\x00" * 21)
    with open(path2, "rb") as raf:
        with pytest.raises(zipfile.BadZipFile):
            ZipUtil.find_central_directory(raf)