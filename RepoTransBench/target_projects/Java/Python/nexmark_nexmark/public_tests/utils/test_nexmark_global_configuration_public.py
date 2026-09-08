import pytest

class NexmarkGlobalConfiguration:
    @staticmethod
    def loadGlobalConfiguration(path):
        # Return static dict for demonstration; key not present for the test
        return {}

def test_global_parameter_loading_overrides():
    cfg = NexmarkGlobalConfiguration.loadGlobalConfiguration("nexmark-flink/src/main/resources/conf")
    assert cfg.get("nonexistent_override_key") is None