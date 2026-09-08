import pytest

class FlinkNexmarkOptions:
    FLINK_REST_PORT = "flink.rest.port"
    FLINK_REST_ADDRESS = "flink.rest.address"

class Configuration(dict):
    def get(self, key, default=None):
        return super().get(key, default)

class NexmarkGlobalConfiguration:
    @staticmethod
    def load_configuration(conf_dir_path):
        # Stub, always return 8081 and 'localhost' (simulate loading)
        config = Configuration()
        config[FlinkNexmarkOptions.FLINK_REST_PORT] = 8081
        config[FlinkNexmarkOptions.FLINK_REST_ADDRESS] = "localhost"
        return config

def test_load_configuration():
    config = NexmarkGlobalConfiguration.load_configuration("fake/path/conf")
    assert config.get(FlinkNexmarkOptions.FLINK_REST_PORT, -1) == 8081
    assert config.get(FlinkNexmarkOptions.FLINK_REST_ADDRESS, "") == "localhost"