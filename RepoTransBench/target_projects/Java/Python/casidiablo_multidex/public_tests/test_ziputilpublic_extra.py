import pytest
import zipfile
import os

def test_zip_entry_no_extra_data_public(tmp_path):
    # Used in ZipUtilExtraPublicTest.java: verify ZipEntry extra with empty and null values
    with zipfile.ZipFile(tmp_path / "xtra2.zip", "w") as z:
        info = zipfile.ZipInfo("anotherfile.txt")
        z.writestr(info, b"abc")
    with zipfile.ZipFile(tmp_path / "xtra2.zip") as z:
        entry = next((ei for ei in z.infolist() if ei.filename == "anotherfile.txt"), None)
        assert entry is not None
        # Python does not expose unset/null extra, but should return b""
        assert hasattr(entry, "extra")
        entry._raw_time = 0
        # .extra is bytes, default empty
        assert isinstance(entry.extra, bytes)
        # Should be empty by default, but after set, can still be zero-length bytes
        # Simulate .setExtra(new byte[0]) with direct assign
        entry.extra = b''
        assert isinstance(entry.extra, bytes)
        assert len(entry.extra) == 0

def test_zip_entry_with_extra_data_public(tmp_path):
    # Used in ZipUtilExtraPublicTest.java: verify set extra data yields correct extra
    filename = tmp_path / "extrastuff2.zip"
    with zipfile.ZipFile(filename, "w") as z:
        info = zipfile.ZipInfo("some_entry.txt")
        info.extra = b"\x2a\x07\x64\x05"
        z.writestr(info, b"zzz")
    with zipfile.ZipFile(filename) as z:
        entry = next((ei for ei in z.infolist() if ei.filename == "some_entry.txt"), None)
        assert entry.extra == b"\x2a\x07\x64\x05"