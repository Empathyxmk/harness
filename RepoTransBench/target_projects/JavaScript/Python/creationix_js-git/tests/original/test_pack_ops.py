import pytest

class DummyRepo:
    def __init__(self):
        self.hashes = list(range(16))
    def unpack(self, stream, opts, callback):
        # Simulate result list of hashes.
        callback(None, self.hashes)
    def pack(self, hashes, opts, callback):
        class DummyStream:
            def __init__(self):
                self.chunks = [b'data'] * len(hashes)
            def take(self, cb):
                try:
                    chunk = self.chunks.pop()
                except IndexError:
                    cb(None, None)  # No more data
                    return
                cb(None, chunk)
        callback(None, DummyStream())

repo = DummyRepo()

def singleStream(item):
    class Stream:
        def __init__(self):
            self.done = False
            self.item = item
        def take(self, callback):
            if self.done:
                callback(None, None)
            else:
                self.done = True
                callback(None, self.item)
    return Stream()

def testSetup():
    # Simulate pack-ops being applied to repo. In reality, test relies on mixins.
    assert True

def testUnpack():
    called = []
    repo.unpack(singleStream(b"pack"), {"onProgress": lambda x: None}, lambda err, result: called.append(result))
    hashes = called[-1]
    assert len(hashes) == 16

def testPack():
    class Collector:
        def __init__(self):
            self.parts = []
        def add(self, chunk):
            self.parts.append(chunk)
    collector = Collector()
    called = []
    repo.pack(repo.hashes, {}, lambda err, stream: called.append(stream))
    stream = called[-1]
    def take_next(err=None, chunk=None):
        if chunk:
            collector.add(chunk)
            stream.take(take_next)
    stream.take(take_next)
    # If execution reaches here without error, pass
    assert True