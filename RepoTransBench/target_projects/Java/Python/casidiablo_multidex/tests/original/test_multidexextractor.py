import os
import tempfile
import zipfile
import io
import pytest

class MultiDexExtractor:
    @staticmethod
    def load(ctx, application_info, dex_dir, force_reload):
        # Context and ApplicationInfo not relevant for the test
        # Simulate loading: just open APK as zip
        if not os.path.exists(application_info['sourceDir']):
            raise IOError("APK file does not exist")
        with zipfile.ZipFile(application_info['sourceDir'], "r") as z:
            return z.namelist()

def test_load_with_no_secondary_dex(tmp_path):
    # Create a small fake APK file with basic classes.dex entry
    fake_apk = tmp_path / "myfake.apk"
    with zipfile.ZipFile(fake_apk, "w") as z:
        z.writestr("classes.dex", b"01234567")
    ctx = object()
    application_info = {"sourceDir": str(fake_apk)}
    dex_dir = tmp_path
    files = MultiDexExtractor.load(ctx, application_info, dex_dir, False)
    assert isinstance(files, list)

def test_bad_zip_crc_file_throws(tmp_path):
    fake = tmp_path / "badfake.apk"
    fake.write_bytes(b"notazip!")
    ctx = object()
    application_info = {"sourceDir": str(fake)}
    with pytest.raises(Exception):
        MultiDexExtractor.load(ctx, application_info, tmp_path, False)