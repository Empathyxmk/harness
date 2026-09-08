import pytest

class PluginConfig:
    pass

class MyPluginEntry:
    def __init__(self):
        self._transformers = None

    def init(self, environment, config):
        # init with environment and config (do nothing)
        self._transformers = []

    def getTransformers(self):
        return self._transformers

    def getName(self):
        return "MyMapPlugin"

    def getAuthor(self):
        return "zfkun"

    def getVersion(self):
        return "1.0.0"

    def getDescription(self):
        return "A plugin for map transformation - example python port."

def test_init_and_getters():
    entry = MyPluginEntry()
    entry.init(None, PluginConfig())
    assert entry.getTransformers() is not None

def test_meta():
    entry = MyPluginEntry()
    assert entry.getName() == "MyMapPlugin"
    assert entry.getAuthor() == "zfkun"
    assert entry.getVersion() == "1.0.0"
    assert "plugin" in entry.getDescription().lower()