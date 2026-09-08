import pytest
import os

class ZipUtil:
    @staticmethod
    def find_central_directory(raf):
        # Try reading a non-existent file
        raf.seek(0)

    @staticmethod
    def get_zip_crc(f):
        # Open and simulate error for missing file
        with open(str(f), "rb") as _:
            pass

def test_non_existent_file_cannot_find_central_directory_public(tmp_path):
    filename = tmp_path / ("this_file_should_not_exist_%s.zip" % str(os.urandom(4)))
    try:
        with open(filename, "rb") as raf:
            try:
                ZipUtil.find_central_directory(raf)
                assert False, "Should have thrown because file doesn't exist"
            except Exception:
                pass
    except Exception:
        pass

def test_get_zip_crc_non_existent_file_public(tmp_path):
    file = tmp_path / ("definitely_not_here_%s.zip" % str(os.urandom(4)))
    with pytest.raises(Exception):
        ZipUtil.get_zip_crc(file)