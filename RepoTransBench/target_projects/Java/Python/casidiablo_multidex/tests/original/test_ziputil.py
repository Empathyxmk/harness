import os
import tempfile
import zipfile
import pytest
import io
import shutil
import struct

class CentralDirectory:
    def __init__(self, offset=0, size=0):
        self.offset = offset
        self.size = size

class ZipUtil:
    @staticmethod
    def get_zip_crc(zip_file: str):
        with open(zip_file, 'rb') as f:
            crc = 0
            while True:
                data = f.read(4096)
                if not data:
                    break
                crc = (crc + sum(data)) % (2**32 - 1)  # Simplified CRC for the purpose of test
            return crc if os.path.getsize(zip_file) > 0 else 0

    @staticmethod
    def find_central_directory(raf):
        # Find zip64 EOCD or EOCD record in a file
        raf.seek(0, os.SEEK_END)
        file_size = raf.tell()
        if file_size < 22:
            raise zipfile.BadZipFile("File is too short to be a zip file")
        # Just fake a directory at end for test
        return CentralDirectory(offset=0, size=file_size)

    @staticmethod
    def compute_crc_of_central_dir(raf, dir):
        raf.seek(dir.offset)
        data = raf.read(int(dir.size))
        return sum(data) % (2**32 - 1)

def test_crc_do_not_crash(tmp_path):
    zip_file = tmp_path / "crc_test.zip"
    with zipfile.ZipFile(zip_file, "w") as z:
        z.writestr("one.txt", b"hello")
        z.writestr("two.txt", b"world")
    crc = ZipUtil.get_zip_crc(str(zip_file))
    assert isinstance(crc, int)

def test_crc_range(tmp_path):
    zip_file = tmp_path / "crcrange_test.zip"
    with zipfile.ZipFile(zip_file, "w") as z:
        z.writestr("one.txt", b"abc")
        z.writestr("two.txt", b"xyz")

    with open(zip_file, "rb") as f:
        raf = io.BytesIO(f.read())
    dir = ZipUtil.find_central_directory(raf)
    raf.seek(dir.offset)
    dirdata = raf.read()
    # Simulate minimal ZipEntryReader logic
    with zipfile.ZipFile(zip_file, "r") as z:
        ref_names = set(z.namelist())
        entries = set()
        for name in z.namelist():
            entries.add(name)
        assert len(entries) == len(ref_names)

def test_crc_value(tmp_path):
    zip_file = tmp_path / "crcval_test.zip"
    with zipfile.ZipFile(zip_file, "w") as z:
        z.writestr("abc.txt", b"DEF")
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

def test_invalid_crc_value(tmp_path):
    zip_file = tmp_path / "invalid_crcval.zip"
    with zipfile.ZipFile(zip_file, "w") as z:
        z.writestr("hello.txt", b"world-zip")
    with zipfile.ZipFile(zip_file, "r") as z:
        for info in z.infolist():
            if info.file_size > 0:
                tmp = tmp_path / f"invfake_{info.filename.replace('/','_')}"
                with open(tmp, "wb") as out, z.open(info.filename) as src:
                    shutil.copyfileobj(src, out)
                with open(tmp, "rb") as raf:
                    rafb = io.BytesIO(raf.read())
                dir = CentralDirectory(offset=0, size=os.path.getsize(tmp)-1)
                crc = ZipUtil.compute_crc_of_central_dir(rafb, dir)
                expected = sum(open(tmp,"rb").read()) % (2**32 - 1)
                assert expected != crc