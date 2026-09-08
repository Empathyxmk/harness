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

def test_version_public(connector):
    assert connector.version() == "1.0"

def test_start_and_task_configs_public(connector):
    props = {"host": "localhost", "port": "5432"}
    connector.start(props)
    configs = connector.taskConfigs(3)
    assert len(configs) == 3
    for conf in configs:
        assert conf is not None
        assert conf.get("host") == "localhost"
        assert conf.get("port") == "5432"

def test_task_class_public(connector):
    assert connector.taskClass() == PostgreSQLSinkTask

def test_stop_public(connector):
    connector.stop()

def test_config_public(connector):
    config_def = connector.config()
    assert config_def is not None