import pytest

class MockSpan:
    def __init__(self, name):
        self.name = name

class OtelBatchExporter:
    def __init__(self, batch_size, batch_count, endpoint):
        self.batch_size = batch_size
        self.batch_count = batch_count
        self.endpoint = endpoint
        self.exported_batches = []
        self.current_batch = []

    def add_span(self, span):
        self.current_batch.append(span)
        if len(self.current_batch) >= self.batch_size:
            self.exported_batches.append(self.current_batch)
            self.current_batch = []

    def flush(self):
        if self.current_batch:
            self.exported_batches.append(self.current_batch)
            self.current_batch = []

def test_batch_exporter_public_handles_different_batch_size_and_content():
    exporter = OtelBatchExporter(5, 2, "http://localhost:33333/")
    span_names = ["spanA", "spanB", "spanC", "spanD", "spanE"]
    for name in span_names:
        exporter.add_span(MockSpan(name))
    assert len(exporter.exported_batches) == 1
    batch = exporter.exported_batches[0]
    assert len(batch) == 5
    assert batch[3].name == "spanD"
    assert batch[4].name == "spanE"

def test_batch_exporter_public_flushes_after_batch_count_timeout():
    exporter = OtelBatchExporter(10, 1, "http://localhost:33334/")
    exporter.add_span(MockSpan("lonespan"))
    exporter.flush()
    assert len(exporter.exported_batches) == 1
    batch = exporter.exported_batches[0]
    assert len(batch) == 1
    assert batch[0].name == "lonespan"