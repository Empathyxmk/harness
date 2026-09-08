import pytest

class FakeURLFilters:
    """
    Mocks URL filtering logic for PreFilterBolt test.
    """
    def __init__(self, return_value):
        self.return_value = return_value
        self.called_with = []

    def filter(self, arg1, arg2, url):
        self.called_with.append(url)
        return self.return_value

class Constants:
    StatusStreamName = "status"

class FakeMetadata(dict):
    def getValues(self, key):
        return [self.get(key)] if key in self else []

    def addValue(self, key, value):
        self[key] = value

class FakeOutputCollector:
    def __init__(self):
        self.emitted = []
        self.acked = []

    def emit(self, *args):
        self.emitted.append(args)

    def ack(self, item):
        self.acked.append(item)

class PreFilterBolt:
    def __init__(self, url_filters):
        self.urlFilters = url_filters

    def prepare(self, config, context, collector):
        self.collector = collector

    def execute(self, tuple):
        url = tuple.get('url')
        metadata = tuple.get('metadata')
        filtered_url = self.urlFilters.filter(None, None, url)
        if filtered_url is None:
            metadata['error.cause'] = 'Filtered'
            self.collector.emit(Constants.StatusStreamName, tuple, ["FILTERED", url, metadata])
            self.collector.ack(tuple)
        else:
            self.collector.emit(tuple, ["ACCEPTED", url, metadata])
            self.collector.ack(tuple)

def tuple_with_url_and_metadata(url, md):
    return {'url': url, 'metadata': md}

def test_url_rejected():
    filters = FakeURLFilters(return_value=None)
    bolt = PreFilterBolt(filters)
    collector = FakeOutputCollector()
    bolt.prepare({}, None, collector)

    md = FakeMetadata()
    input_tuple = tuple_with_url_and_metadata("http://reject.me", md)
    bolt.execute(input_tuple)

    assert (Constants.StatusStreamName, input_tuple, ["FILTERED", "http://reject.me", md]) in collector.emitted
    assert input_tuple in collector.acked
    assert md.get('error.cause') == 'Filtered'

def test_url_accepted():
    filters = FakeURLFilters(return_value="http://accept.me")
    bolt = PreFilterBolt(filters)
    collector = FakeOutputCollector()
    bolt.prepare({}, None, collector)

    md = FakeMetadata()
    input_tuple = tuple_with_url_and_metadata("http://accept.me", md)
    bolt.execute(input_tuple)

    # Should not emit to the status stream, only emit accepted
    assert any(args[0] == input_tuple for args in collector.emitted)
    assert all(args[0] != Constants.StatusStreamName for args in collector.emitted)
    assert input_tuple in collector.acked