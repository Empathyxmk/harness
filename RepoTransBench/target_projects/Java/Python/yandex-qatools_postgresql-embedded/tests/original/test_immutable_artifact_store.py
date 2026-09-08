import pytest

class IMutableArtifactStore:
    def set_download_config(self, download_config):
        raise NotImplementedError()
    def remove_file_set(self, d, fs):
        raise NotImplementedError()
    def check_distribution(self, d):
        raise NotImplementedError()
    def extract_file_set(self, d):
        raise NotImplementedError()

class TestMutableArtifactStore(IMutableArtifactStore):
    def __init__(self):
        self.config_set = False
    def set_download_config(self, download_config):
        self.config_set = True
    def remove_file_set(self, d, fs):
        pass
    def check_distribution(self, d):
        return False
    def extract_file_set(self, d):
        return None

def test_set_download_config():
    store = TestMutableArtifactStore()
    assert not store.config_set
    store.set_download_config(None)
    assert store.config_set