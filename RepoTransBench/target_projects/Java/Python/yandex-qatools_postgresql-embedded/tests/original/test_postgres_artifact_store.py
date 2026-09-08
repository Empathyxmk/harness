import os
import tempfile
import shutil
import pytest

class LocalArtifactStore:
    @staticmethod
    def check_artifact(download_config, dist):
        return getattr(dist, 'has_artifact', False)
    @staticmethod
    def store(download_config, dist, file):
        # Pretend to store always succeeds
        return True

class PostgresArtifactStore:
    def __init__(self, download_config, dir_factory, temp_naming, downloader):
        self._download_config = download_config
        self._dir_factory = dir_factory
        self._temp_naming = temp_naming
        self._downloader = downloader

    def get_download_config(self):
        return self._download_config

    def set_download_config(self, new_cfg):
        self._download_config = new_cfg

    def remove_file_set(self, distribution, file_set):
        # Try deleting files
        for f in file_set.files():
            if os.path.exists(f):
                os.unlink(f)
        if file_set.base_dir_is_generated():
            base_dir = file_set.base_dir()
            if os.path.exists(base_dir) and os.path.isdir(base_dir):
                try:
                    shutil.rmtree(base_dir)
                except Exception:
                    pass

    def check_distribution(self, dist):
        if not LocalArtifactStore.check_artifact(self._download_config, dist):
            # simulate download/store
            _ = self._downloader.download(self._download_config, dist)
            return LocalArtifactStore.store(self._download_config, dist, "somefile")
        else:
            return True

    def extract_file_set(self, distribution):
        # Just simulate: always returns 'EmptyFileSet' on error
        try:
            # imagine extracting, but possible error
            raise Exception("Fail!")
        except Exception:
            return "EmptyFileSet"

class DummyFileSet:
    def __init__(self, temp_files):
        self._files = temp_files
    def files(self):
        return self._files
    def executable(self):
        return None
    def base_dir_is_generated(self):
        return True
    def base_dir(self):
        return os.path.dirname(self._files[0])

class DummyDownloader:
    def download(self, download_config, dist):
        # Just pretend it downloads something to file
        return "somefile"

def test_set_and_get_download_config():
    store = PostgresArtifactStore(object(), object(), object(), object())
    cfg2 = object()
    store.set_download_config(cfg2)
    assert store.get_download_config() == cfg2

def test_remove_file_set_deletes_files(tmp_path):
    tmp_file = tmp_path / "toDel.bin"
    tmp_file.write_bytes(b"ok")
    file_set = DummyFileSet([str(tmp_file)])
    store = PostgresArtifactStore(object(), object(), object(), object())
    # Should not raise an error
    store.remove_file_set(object(), file_set)
    assert not tmp_file.exists()

def test_check_distribution_false_then_store():
    class MockDist:
        pass

    download_config = object()
    dist = MockDist()
    dist.has_artifact = False
    store = PostgresArtifactStore(download_config, object(), object(), DummyDownloader())
    ok = store.check_distribution(dist)
    assert ok

def test_check_distribution_true():
    class MockDist:
        pass

    download_config = object()
    dist = MockDist()
    dist.has_artifact = True
    store = PostgresArtifactStore(download_config, object(), object(), DummyDownloader())
    ok = store.check_distribution(dist)
    assert ok

def test_extract_file_set_handles_exception():
    store = PostgresArtifactStore(object(), object(), object(), object())
    res = store.extract_file_set(object())
    assert res == "EmptyFileSet"