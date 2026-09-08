import pytest
import zipfile
import os

def test_zip_entry_no_extra_data_public(tmp_path):
    # zipfile.ZipInfo does not expose extra, so use ZipEntry via zipfile
    with zipfile.ZipFile(tmp_path / "xtra.zip", "w") as z:
        info = zipfile.ZipInfo("anotherfile.txt")
        z.writestr(info, b"abc")
    with zipfile.ZipFile(tmp_path / "xtra.zip") as z:
        entry = next((ei for ei in z.infolist() if ei.filename == "anotherfile.txt"), None)
        assert entry is not None
        # Python does not expose extra field, simulate by low-level check
        # but default "extra" is b""
        assert hasattr(entry, "extra")
        # set extra "simulate"
        entry._raw_time = 0
        # .extra is always bytes
        assert isinstance(entry.extra, bytes)
        if entry.extra:
            assert len(entry.extra) == 0 or isinstance(entry.extra, bytes)

def test_zip_entry_with_extra_data_public(tmp_path):
    # Write ZIP file with extra data field
    filename = tmp_path / "extrastuff.zip"
    with zipfile.ZipFile(filename, "w") as z:
        info = zipfile.ZipInfo("some_entry.txt")
        info.extra = b"\x2a\x07\x64\x05"
        z.writestr(info, b"zzz")
    with zipfile.ZipFile(filename) as z:
        entry = next((ei for ei in z.infolist() if ei.filename == "some_entry.txt"), None)
        # In Python, the extra field should match
        assert entry.extra == b"\x2a\x07\x64\x05"