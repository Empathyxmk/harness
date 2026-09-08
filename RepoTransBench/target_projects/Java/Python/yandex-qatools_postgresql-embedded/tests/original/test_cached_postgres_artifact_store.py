import os
import tempfile
import pytest

class CachedPostgresArtifactStore:
    def __init__(self, download_config, dir_factory, temp_naming, downloader):
        self.download_config = download_config
        self.dir_factory = dir_factory
        self.temp_naming = temp_naming
        self.downloader = downloader

    def remove_file_set(self, distribution, file_set):
        # The spec: just does nothing.
        pass

    def extract_file_set(self, distribution):
        # If download_config.get_package_resolver throws, return EmptyFileSet
        try:
            self.download_config.get_package_resolver()
        except Exception:
            return "EmptyFileSet"
        return "SomeFileSet"

class DummyDownloadConfig:
    def get_package_resolver(self):
        return object()

class FailingDownloadConfig:
    def get_package_resolver(self):
        raise RuntimeError("fail!")

def test_remove_file_set_does_nothing():
    store = CachedPostgresArtifactStore(
        DummyDownloadConfig(), object(), object(), object()
    )
    # Should not raise
    store.remove_file_set(object(), object())

def test_extract_file_set_handles_exception_and_returns_empty_file_set():
    store = CachedPostgresArtifactStore(
        FailingDownloadConfig(), object(), object(), object()
    )
    res = store.extract_file_set(object())
    assert res == "EmptyFileSet"