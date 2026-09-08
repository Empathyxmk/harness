import pytest
from unittest.mock import MagicMock, patch, call

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
        mapping = {}
        if config.get('messageRoutingMode', '').lower() == 'custompartition':
            mapping['messageRoutingMode'] = "CustomPartition"
        if config.get('hashingScheme', '').lower() == 'murmur3_32hash':
            mapping['hashingScheme'] = "Murmur3_32Hash"
        if config.get('cryptoFailureAction', '').lower() == 'send':
            mapping['cryptoFailureAction'] = "SEND"
        if config.get('compressionType', '').lower() == 'zlib':
            mapping['compressionType'] = "ZLIB"
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

def test_configure_and_init_producer_public():
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

def test_init_producer_load_config_branches_public():
    sink = DummyPulsarSink()
    config = {
        "messageRoutingMode": "custompartition",
        "hashingScheme": "murmur3_32hash",
        "cryptoFailureAction": "send",
        "compressionType": "zlib"
    }
    res = sink.initProducerLoadConfig(config)
    assert res['messageRoutingMode'] == "CustomPartition"
    assert 'messageRoutingMode' in res or 'hashingScheme' in res
    assert res['cryptoFailureAction'] == "SEND"
    assert res['compressionType'] == "ZLIB"

def test_process_and_stop_public():
    sink = DummyPulsarSink()
    producer = MagicMock()
    client = MagicMock()
    sink.pulsarProducer = producer
    sink.pulsarClient = client
    msg = MagicMock()
    msg.getHeaders().getString.return_value = "publicHeaderVal"
    msg.getPayload.return_value = "otherpayload"
    sink.process([msg])
    producer.send.assert_called_once_with("otherpayload")
    sink.stop()
    client.close.assert_called_once()