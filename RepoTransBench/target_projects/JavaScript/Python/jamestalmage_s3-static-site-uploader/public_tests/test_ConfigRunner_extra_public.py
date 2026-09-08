import pytest

class DummyConfigRunner:
    def __init__(self, config):
        self.config = config

    def run(self):
        if self.config.get("fail", False):
            raise ValueError("DummyConfigRunner failed")
        return "public success"

def test_configrunner_runs_publicly():
    runner = DummyConfigRunner({"public": True})
    result = runner.run()
    assert result == "public success"

def test_configrunner_public_fail():
    runner = DummyConfigRunner({"fail": True})
    with pytest.raises(ValueError) as excinfo:
        runner.run()
    assert "DummyConfigRunner failed" in str(excinfo.value)