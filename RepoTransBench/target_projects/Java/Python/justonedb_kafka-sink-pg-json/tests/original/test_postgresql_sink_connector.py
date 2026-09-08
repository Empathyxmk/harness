import pytest

class PostgreSQLSinkTask:
    pass

class ConfigDef:
    pass

class PostgreSQLSinkConnector:
    def version(self):
        return "1.0"

    def start(self, props):
        self.props = props

    def taskConfigs(self, n):
        # Return a list of n dicts, each copy of self.props
        return [self.props.copy() for _ in range(n)]

    def taskClass(self):
        return PostgreSQLSinkTask

    def stop(self):
        pass

    def config(self):
        return ConfigDef()

import pytest

@pytest.fixture
def connector():
    return PostgreSQLSinkConnector()

def test_version(connector):
    assert connector.version() == "1.0"

def test_start_and_task_configs(connector):
    props = {"foo": "bar"}
    connector.start(props)
    configs = connector.taskConfigs(2)
    assert len(configs) == 2
    for conf in configs:
        assert conf is not None
        assert conf.get("foo") == "bar"

def test_task_class(connector):
    assert connector.taskClass() == PostgreSQLSinkTask

def test_stop(connector):
    connector.stop()

def test_config(connector):
    config_def = connector.config()
    assert config_def is not None