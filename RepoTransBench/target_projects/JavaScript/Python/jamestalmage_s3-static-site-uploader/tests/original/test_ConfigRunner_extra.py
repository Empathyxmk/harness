import pytest

class DummyConfigRunner:
    def __init__(self, config):
        self.config = config
        self.ran = False

    def run(self):
        if not self.config.get("run_should_fail", False):
            self.ran = True
            return "success"
        else:
            raise Exception("ConfigRunner run failed")


def test_configrunner_runs_successfully():
    runner = DummyConfigRunner({"some_key": "some_val"})
    result = runner.run()
    assert result == "success"
    assert runner.ran is True

def test_configrunner_run_fails_on_flag():
    runner = DummyConfigRunner({"run_should_fail": True})
    with pytest.raises(Exception) as excinfo:
        runner.run()
    assert "ConfigRunner run failed" in str(excinfo.value)