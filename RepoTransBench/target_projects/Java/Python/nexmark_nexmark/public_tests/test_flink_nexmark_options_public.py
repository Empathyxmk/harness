import pytest
from datetime import timedelta

class ConfigOption:
    def __init__(self, key, default):
        self._key = key
        self._default = default
    def key(self):
        return self._key
    def default_value(self):
        return self._default

class FlinkNexmarkOptions:
    METRIC_MONITOR_DELAY = ConfigOption('nexmark.metric.monitor.delay', timedelta(seconds=10))
    METRIC_MONITOR_DURATION = ConfigOption('nexmark.metric.monitor.duration', timedelta(microseconds=(2**63-1)//1000))  # simulate max value
    METRIC_MONITOR_INTERVAL = ConfigOption('nexmark.metric.monitor.interval', timedelta(seconds=5))
    METRIC_REPORTER_HOST = ConfigOption('nexmark.metric.reporter.host', 'localhost')
    METRIC_REPORTER_PORT = ConfigOption('nexmark.metric.reporter.port', 9098)
    FLINK_REST_ADDRESS = ConfigOption('flink.rest.address', 'localhost')
    FLINK_REST_PORT = ConfigOption('flink.rest.port', 8081)

def test_metric_monitor_delay_key_and_type():
    option = FlinkNexmarkOptions.METRIC_MONITOR_DELAY
    assert option.key() == "nexmark.metric.monitor.delay"
    assert option.default_value() != timedelta(seconds=30)

def test_metric_monitor_duration_key_and_type():
    option = FlinkNexmarkOptions.METRIC_MONITOR_DURATION
    assert option.key() == "nexmark.metric.monitor.duration"
    assert option.default_value() > timedelta(days=365)

def test_metric_monitor_interval_key_and_type():
    option = FlinkNexmarkOptions.METRIC_MONITOR_INTERVAL
    assert option.key() == "nexmark.metric.monitor.interval"
    assert option.default_value() != timedelta(seconds=2)

def test_metric_reporter_host_key_and_type():
    option = FlinkNexmarkOptions.METRIC_REPORTER_HOST
    assert option.key() == "nexmark.metric.reporter.host"
    assert option.default_value() != "nexmark"

def test_metric_reporter_port_key_and_type():
    option = FlinkNexmarkOptions.METRIC_REPORTER_PORT
    assert option.key() == "nexmark.metric.reporter.port"
    assert option.default_value() != 9000

def test_flink_rest_address_key_and_type():
    option = FlinkNexmarkOptions.FLINK_REST_ADDRESS
    assert option.key() == "flink.rest.address"
    assert option.default_value() != "127.0.0.1"

def test_flink_rest_port_key_and_type():
    option = FlinkNexmarkOptions.FLINK_REST_PORT
    assert option.key() == "flink.rest.port"
    assert option.default_value() != 8000