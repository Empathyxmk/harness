import pytest

class NonCachedPostgresArtifactStoreBuilder:
    def __init__(self):
        self._download_config = None
        self._temp_dir_factory = None
        self._executable_naming = None
        self._downloader = None

    def download_config(self, val):
        self._download_config = val
        return self

    def temp_dir_factory(self, val):
        self._temp_dir_factory = val
        return self

    def executable_naming(self, val):
        self._executable_naming = val
        return self

    def downloader(self, val):
        self._downloader = val
        return self

    def build(self):
        return PostgresArtifactStore()

class PostgresArtifactStore:
    pass

def test_builder_should_return_postgres_artifact_store():
    builder = NonCachedPostgresArtifactStoreBuilder()
    download_config = object()
    dir_factory = object()
    temp_naming = object()
    downloader = object()
    builder.download_config(download_config).temp_dir_factory(dir_factory).executable_naming(temp_naming).downloader(downloader)
    store = builder.build()
    assert isinstance(store, PostgresArtifactStore)