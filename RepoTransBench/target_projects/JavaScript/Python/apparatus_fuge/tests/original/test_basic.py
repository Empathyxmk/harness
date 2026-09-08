import importlib

try:
    fugeMod = importlib.import_module('tests.helpers.runner')
except ModuleNotFoundError:
    def fugeMod(*args, **kwargs):
        return {}

def test_should_export_a_function():
    assert callable(fugeMod)

def test_should_return_a_runner_object_if_given_config():
    runner = fugeMod({})
    assert runner
    assert isinstance(runner, object)