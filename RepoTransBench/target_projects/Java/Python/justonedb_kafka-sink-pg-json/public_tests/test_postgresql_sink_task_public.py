import pytest

class SinkRecord:
    def __init__(self, topic, partition, key_schema, key, value_schema, value, offset):
        self.topic = topic
        self.partition = partition
        self.key_schema = key_schema
        self.key = key
        self.value_schema = value_schema
        self.value = value
        self.offset = offset

class PostgreSQLSinkTask:
    def version(self):
        return "1.0"

    def start(self, props):
        self.props = props

    def stop(self):
        pass

    def put(self, records):
        # Accept a list of SinkRecord, for test
        pass

import pytest

@pytest.fixture
def task():
    return PostgreSQLSinkTask()

def test_version_public(task):
    assert task.version() == "1.0"

def test_start_and_stop_public(task):
    props = {"username": "alice", "password": "securepass"}
    task.start(props)
    task.stop()

def test_put_public(task):
    records = []
    records.append(SinkRecord("public_topic", 1, None, None, None, None, 123))
    task.put(records)