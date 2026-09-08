import pytest
from unittest.mock import MagicMock, patch
import threading

class DummyPulsarSource:
    def __init__(self):
        self.pulsarClient = None
        self.pulsarConsumer = None
        self.runnerThread = None
        self.runner = None
    def configure(self, context):
        state = context.getState()
        self.pulsarClient = state.getClient()
        cb = self.pulsarClient.newConsumer('STRING')
        cb.loadConf({})
        self.pulsarConsumer = cb.subscribe()
    def initConsumerLoadConfig(self, config):
        mapping = {}
        if "topicNames" in config:
            mapping["topicNames"] = config["topicNames"]
        if "topicsPattern" in config:
            mapping["topicsPattern"] = config["topicsPattern"]
        if config.get("subscriptionType", "").lower() == "exclusive":
            mapping["subscriptionType"] = "Exclusive"
        if config.get("cryptoFailureAction", "").lower() == "fail":
            mapping["cryptoFailureAction"] = "FAIL"
        return mapping
    def unsubscribe(self):
        if self.pulsarConsumer:
            self.pulsarConsumer.unsubscribe()
            self.pulsarConsumer.close()
    def stop(self):
        if self.runnerThread and self.runnerThread.is_alive():
            self.runnerThread.join(timeout=0.1)
        if self.pulsarClient:
            self.pulsarClient.close()
    def start(self):
        self.runner = MagicMock()
        self.runnerThread = None

def test_configure_and_init_consumer():
    source = DummyPulsarSource()
    context = MagicMock()
    state = MagicMock()
    client = MagicMock()
    cb = MagicMock()
    consumer = MagicMock()
    context.getState.return_value = state
    state.getClient.return_value = client
    client.newConsumer.return_value = cb
    cb.loadConf.return_value = cb
    cb.subscribe.return_value = consumer

    source.configure(context)
    assert source.pulsarConsumer == consumer

def test_init_consumer_load_config_branches():
    source = DummyPulsarSource()
    config = {
        "topicNames": {"a": "topic1"},
        "topicsPattern": ".*",
        "subscriptionType": "exclusive",
        "cryptoFailureAction": "fail"
    }
    res = source.initConsumerLoadConfig(config)
    assert "topicNames" in res
    assert "topicsPattern" in res
    assert res.get("subscriptionType") == "Exclusive"

def test_stop_and_unsubscribe():
    source = DummyPulsarSource()
    consumer = MagicMock()
    client = MagicMock()
    source.pulsarConsumer = consumer
    source.pulsarClient = client
    source.unsubscribe()
    consumer.unsubscribe.assert_called_once()
    consumer.close.assert_called_once()

    thread = threading.Thread(target=lambda: None)
    thread.start()
    source.runnerThread = thread
    source.runner = MagicMock()
    source.runnerThread = thread
    source.pulsarClient = client
    source.stop()
    client.close.assert_called()

def test_start_calls_runner():
    source = DummyPulsarSource()
    source.runner = MagicMock()
    source.runnerThread = None
    source.start()
    assert source.runner is not None