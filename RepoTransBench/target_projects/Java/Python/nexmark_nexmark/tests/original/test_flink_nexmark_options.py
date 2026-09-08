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
    METRIC_MONITOR_DURATION = ConfigOption('nexmark.metric.monitor.duration', timedelta(microseconds=(2**63-1)//1000))  # Long.MAX_VALUE ns as rough max, fallback
    METRIC_MONITOR_INTERVAL = ConfigOption('nexmark.metric.monitor.interval', timedelta(seconds=5))
    METRIC_REPORTER_HOST = ConfigOption('nexmark.metric.reporter.host', 'localhost')
    METRIC_REPORTER_PORT = ConfigOption('nexmark.metric.reporter.port', 9098)
    FLINK_REST_ADDRESS = ConfigOption('flink.rest.address', 'localhost')
    FLINK_REST_PORT = ConfigOption('flink.rest.port', 8081)

def test_metric_monitor_delay_defaults():
    option = FlinkNexmarkOptions.METRIC_MONITOR_DELAY
    assert option.key() == "nexmark.metric.monitor.delay"
    assert option.default_value() == timedelta(seconds=10)

def test_metric_monitor_duration_defaults():
    option = FlinkNexmarkOptions.METRIC_MONITOR_DURATION
    assert option.key() == "nexmark.metric.monitor.duration"
    # Accepting a huge value as default
    assert option.default_value() == timedelta(microseconds=(2**63-1)//1000)

def test_metric_monitor_interval_defaults():
    option = FlinkNexmarkOptions.METRIC_MONITOR_INTERVAL
    assert option.key() == "nexmark.metric.monitor.interval"
    assert option.default_value() == timedelta(seconds=5)

def test_metric_reporter_host_defaults():
    option = FlinkNexmarkOptions.METRIC_REPORTER_HOST
    assert option.key() == "nexmark.metric.reporter.host"
    assert option.default_value() == "localhost"

def test_metric_reporter_port_defaults():
    option = FlinkNexmarkOptions.METRIC_REPORTER_PORT
    assert option.key() == "nexmark.metric.reporter.port"
    assert option.default_value() == 9098

def test_flink_rest_address_defaults():
    option = FlinkNexmarkOptions.FLINK_REST_ADDRESS
    assert option.key() == "flink.rest.address"
    assert option.default_value() == "localhost"

def test_flink_rest_port_defaults():
    option = FlinkNexmarkOptions.FLINK_REST_PORT
    assert option.key() == "flink.rest.port"
    assert option.default_value() == 8081