import pytest
from unittest.mock import MagicMock, patch, call
import types

class DummyPulsarSink:
    def __init__(self):
        self.pulsarProducer = None
        self.pulsarClient = None
    def configure(self, context):
        state = context.getState()
        self.pulsarClient = state.getClient()
        pb = self.pulsarClient.newProducer()
        pb.loadConf({})
        self.pulsarProducer = pb.create()
    def initProducerLoadConfig(self, config):
        # Convert values as in Java.
        mapping = {}
        if config.get('messageRoutingMode', '').lower() == 'roundrobinpartition':
            mapping['messageRoutingMode'] = "RoundRobinPartition"
        if config.get('hashingScheme', '').lower() == 'javastringhash':
            mapping['hashingScheme'] = "JavaStringHash"
        if config.get('cryptoFailureAction', '').lower() == 'fail':
            mapping['cryptoFailureAction'] = "FAIL"
        if config.get('compressionType', '').lower() == 'lz4':
            mapping['compressionType'] = "LZ4"
        return mapping
    def process(self, messages):
        for msg in messages:
            topic = msg.getHeaders().getString("topic")
            if not topic:
                continue
            payload = msg.getPayload()
            self.pulsarProducer.send(payload)
    def stop(self):
        if self.pulsarClient:
            self.pulsarClient.close()

def test_configure_and_init_producer():
    sink = DummyPulsarSink()
    context = MagicMock()
    state = MagicMock()
    client = MagicMock()
    pb = MagicMock()
    producer = MagicMock()
    context.getState.return_value = state
    state.getClient.return_value = client
    client.newProducer.return_value = pb
    pb.loadConf.return_value = pb
    pb.create.return_value = producer

    sink.configure(context)
    assert sink.pulsarProducer == producer

def test_init_producer_load_config_branches():
    sink = DummyPulsarSink()
    config = {
        "messageRoutingMode": "roundrobinpartition",
        "hashingScheme": "javastringhash",
        "cryptoFailureAction": "fail",
        "compressionType": "lz4"
    }
    res = sink.initProducerLoadConfig(config)
    assert res['messageRoutingMode'] == "RoundRobinPartition"
    assert res['hashingScheme'] == "JavaStringHash"
    assert res['cryptoFailureAction'] == "FAIL"
    assert res['compressionType'] == "LZ4"

def test_process_and_stop():
    sink = DummyPulsarSink()
    producer = MagicMock()
    client = MagicMock()
    sink.pulsarProducer = producer
    sink.pulsarClient = client
    msg1 = MagicMock()
    msg2 = MagicMock()
    msg1.getHeaders().getString.return_value = ""
    msg2.getHeaders().getString.return_value = "topic"
    msg1.getPayload.return_value = "payload1"
    msg2.getPayload.return_value = "payload2"
    sink.process([msg1, msg2])
    producer.send.assert_called_once_with("payload2")
    sink.stop()
    client.close.assert_called_once()