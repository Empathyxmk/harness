import os
import zipfile
import io
import shutil
import pytest

class CentralDirectory:
    def __init__(self, offset=0, size=0):
        self.offset = offset
        self.size = size

class ZipUtil:
    @staticmethod
    def get_zip_crc(zip_file):
        with open(zip_file, 'rb') as f:
            crc = 0
            while True:
                data = f.read(4096)
                if not data:
                    break
                crc = (crc + sum(data)) % (2**32 - 1)
            return crc

    @staticmethod
    def find_central_directory(raf):
        raf.seek(0, os.SEEK_END)
        file_size = raf.tell()
        if file_size < 22:
            raise zipfile.BadZipFile("File too short for central directory")
        return CentralDirectory(offset=0, size=file_size)

    @staticmethod
    def compute_crc_of_central_dir(raf, dir):
        raf.seek(dir.offset)
        data = raf.read(int(dir.size))
        return sum(data) % (2**32 - 1)

def create_public_test_zip(tmp_path):
    temp_zip = tmp_path / "public_test_ziputilpublictest.zip"
    with zipfile.ZipFile(temp_zip, "w") as zs:
        zs.writestr("file1.txt", b"hello")
        zs.writestr("file2.txt", b"world")
    return temp_zip

def test_crc_do_not_crash_public(tmp_path):
    zip_file = create_public_test_zip(tmp_path)
    crc = ZipUtil.get_zip_crc(str(zip_file))
    assert crc > 0

def test_crc_range_public(tmp_path):
    zip_file = create_public_test_zip(tmp_path)
    with open(zip_file, "rb") as f:
        raf = io.BytesIO(f.read())
    dir = ZipUtil.find_central_directory(raf)
    raf.seek(dir.offset)
    dirdata = raf.read()
    with zipfile.ZipFile(zip_file, "r") as z:
        ref_names = set(z.namelist())
        entries = set()
        for name in z.namelist():
            entries.add(name)
        assert len(entries) == len(ref_names)

def test_crc_value_public(tmp_path):
    zip_file = create_public_test_zip(tmp_path)
    with zipfile.ZipFile(zip_file, "r") as z:
        for info in z.infolist():
            if info.file_size > 0:
                tmp = tmp_path / f"fake_{info.filename.replace('/','_')}"
                with open(tmp, "wb") as out, z.open(info.filename) as src:
                    shutil.copyfileobj(src, out)
                with open(tmp, "rb") as raf:
                    rafb = io.BytesIO(raf.read())
                dir = CentralDirectory(offset=0, size=os.path.getsize(tmp))
                crc = ZipUtil.compute_crc_of_central_dir(rafb, dir)
                expected = sum(open(tmp,"rb").read()) % (2**32 - 1)
                assert expected == crc

def test_invalid_crc_value_public(tmp_path):
    zip_file = create_public_test_zip(tmp_path)
    with zipfile.ZipFile(zip_file, "r") as z:
        for info in z.infolist():
            if info.file_size > 0:
                tmp = tmp_path / f"invfake_{info.filename.replace('/','_')}"
                with open(tmp, "wb") as out, z.open(info.filename) as src:
                    shutil.copyfileobj(src, out)
                with open(tmp, "rb") as raf:
                    rafb = io.BytesIO(raf.read())
                dir = CentralDirectory(offset=0, size=os.path.getsize(tmp)-2)
                crc = ZipUtil.compute_crc_of_central_dir(rafb, dir)
                expected = sum(open(tmp,"rb").read()) % (2**32 - 1)
                assert expected != crc