import pytest

class DummyBuilder:
    def __init__(self):
        self.config = None

    def custom_config(self, config):
        self.config = config
        return self

    def get_config(self):
        return self.config

def test_sets_custom_config_different_from_private_test():
    builder = DummyBuilder().custom_config("public_config_4567")
    assert builder.get_config() == "public_config_4567"

def test_config_is_null_by_default():
    builder = DummyBuilder()
    assert builder.get_config() is None